import hashlib
from decimal import Decimal
from typing import BinaryIO

from django.core.files import File
from django.db import transaction

from ..domain.types import ParsedTx
from ..importers.mbank import read_mbank_statement_stream
from ..models import RawTransaction


import logging
logger = logging.getLogger(__name__)


def compute_fingerprint(tx: ParsedTx) -> str:
    # deterministic; tweak if your bank exports unstable fields
    material = "|".join(
        [
            tx.date.isoformat(),
            tx.description,
            tx.this_account_number,
            tx.other_account_name or "",
            tx.other_account_number or "",
            str(tx.amount.quantize(Decimal("0.01"))),
            tx.currency,
        ]
    )
    return hashlib.sha256(material.encode("utf-8")).hexdigest()



@transaction.atomic
def import_transactions_csv(buffer: BinaryIO) -> dict:
    logger.info("import: start")

    parsed = list(read_mbank_statement_stream(buffer))

    logger.info("import: parsed=%d", len(parsed))

    # de-dupe within the uploaded file itself
    seen = {}
    for tx in parsed:
        fp = compute_fingerprint(tx)
        if fp not in seen:
            seen[fp] = (tx, fp)

    fingerprints = list(seen.keys())

    # skip already-existing fingerprints in DB (fast, single query)
    existing = set(
        RawTransaction.objects.filter(fingerprint__in=fingerprints)
        .values_list("fingerprint", flat=True)
    )

    to_create = []
    for fp, (tx, _) in seen.items():
        if fp in existing:
            continue
        to_create.append(
            RawTransaction(
                date=tx.date,
                description=tx.description,
                this_account_number=tx.this_account_number,
                other_account_name=tx.other_account_name,
                other_account_number=tx.other_account_number,
                amount=tx.amount,
                currency=tx.currency,
                fingerprint=fp,
                raw_payload=tx.raw_payload,
            )
        )

    logger.info("import: to_create=%d (duplicates=%d)", len(to_create), len(seen) - len(to_create))

    RawTransaction.objects.bulk_create(to_create, batch_size=1000)

    logger.info("import: done created=%d", len(to_create))

    return {
        "parsed": len(parsed),
        "unique_in_file": len(seen),
        "created": len(to_create),
        "duplicates": len(seen) - len(to_create),
    }