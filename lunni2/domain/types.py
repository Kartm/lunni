import datetime
import uuid
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class ParsedTx:
    date: datetime.date
    description: str
    this_account_number: str
    other_account_name: str | None
    other_account_number: str | None
    amount: Decimal
    currency: str
    raw_payload: dict


@dataclass(frozen=True)
class EffectiveRow:
    kind: str  # "TX" or "GROUP"
    row_id: str  # stable id for UI (e.g. "tx:123" or "group:<uuid>")
    date: datetime.date
    description: str
    amount: Decimal
    currency: str

    # for group only
    group_id: uuid.UUID | None = None # todo why would I need it?!
    tx_id: int | None = None # todo why would I need it?!

    category_id: int | None = None
    category_name: str | None = None
    category_kind: str | None = None  # POS/NEG/IGN
    category_css: str | None = None  # css class - cat-none etc.


@dataclass(frozen=True)
class Selection:
    tx_ids: set[int]
    group_ids: set[uuid.UUID]


@dataclass(frozen=True)
class SelectedItem:
    kind: str  # "tx" | "group"
    id: str    # str for template
    label: str
    amount: Decimal
    currency: str

@dataclass(frozen=True)
class SelectionSummary:
    items: list[SelectedItem]
    total: Decimal | None
    currency: str | None
    tx_count: int
    group_count: int
    mode: str  # "NONE" | "CREATE_GROUP" | "ADD_TO_GROUP" | "MERGE_ALL"
    add_to_group_name: str | None
    errors: list[str]