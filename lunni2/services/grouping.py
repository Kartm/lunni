import uuid
from django.db import transaction
from django.core.exceptions import ValidationError

from ..models import RawTransaction, DomainEvent


def _emit(*, type: str, stream_key: str, payload: dict) -> DomainEvent:
    return DomainEvent.objects.create(type=type, stream_key=stream_key, payload=payload)


def _group_stream(group_id: uuid.UUID) -> str:
    return f"group:{group_id}"


def _validate_same_currency(tx_qs, currency: str | None = None) -> str:
    currencies = set(tx_qs.values_list("currency", flat=True))
    if len(currencies) == 0:
        raise ValidationError("No transactions selected.")
    if len(currencies) > 1:
        raise ValidationError(f"All transactions in a group must share currency. Got: {sorted(currencies)}")
    only = next(iter(currencies))
    if currency is not None and only != currency:
        raise ValidationError(f"Group currency mismatch: expected {currency}, got {only}")
    return only


@transaction.atomic
def create_group(*, title: str, tx_ids: list[int]) -> uuid.UUID:
    txs = RawTransaction.objects.filter(id__in=tx_ids)
    currency = _validate_same_currency(txs)

    group_id = uuid.uuid4()
    stream_key = _group_stream(group_id)

    _emit(
        type=DomainEvent.Type.GROUP_CREATED,
        stream_key=stream_key,
        payload={"group_id": str(group_id), "title": title, "currency": currency},
    )
    _emit(
        type=DomainEvent.Type.GROUP_MEMBERS_ADDED,
        stream_key=stream_key,
        payload={"group_id": str(group_id), "tx_ids": list(txs.values_list("id", flat=True))},
    )
    return group_id


@transaction.atomic
def add_group_members(*, group_id: uuid.UUID, tx_ids: list[int]) -> None:
    stream_key = _group_stream(group_id)

    # read group currency from first GROUP_CREATED event
    created = (
        DomainEvent.objects.filter(stream_key=stream_key, type=DomainEvent.Type.GROUP_CREATED)
        .order_by("created_at", "id")
        .first()
    )
    if not created:
        raise ValidationError("Group does not exist.")

    group_currency = created.payload["currency"]

    txs = RawTransaction.objects.filter(id__in=tx_ids)
    _validate_same_currency(txs, currency=group_currency)

    _emit(
        type=DomainEvent.Type.GROUP_MEMBERS_ADDED,
        stream_key=stream_key,
        payload={"group_id": str(group_id), "tx_ids": list(txs.values_list("id", flat=True))},
    )


@transaction.atomic
def remove_group_members(*, group_id: uuid.UUID, tx_ids: list[int]) -> None:
    stream_key = _group_stream(group_id)

    _emit(
        type=DomainEvent.Type.GROUP_MEMBERS_REMOVED,
        stream_key=stream_key,
        payload={"group_id": str(group_id), "tx_ids": tx_ids},
    )