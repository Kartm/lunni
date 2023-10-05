import io
from typing import BinaryIO, Iterable

from ..domain.types import ParsedTx
import polars as pl

import logging
logger = logging.getLogger(__name__)

def read_mbank_statement_stream(buffer: BinaryIO) -> Iterable[ParsedTx]:
    # Parses mBank Windows-1250 statement stream. Does not close the stream (caller owns it).

    txt = io.TextIOWrapper(buffer, encoding="cp1250", newline="")

    currency: str | None = None
    this_account_number: str | None = None
    pending_currency = False
    pending_account = False
    in_table = False
    buf = io.StringIO()

    total_lines = 0
    table_lines = 0

    for raw_line in txt:
        total_lines += 1
        line = raw_line.strip("\r\n\t")

        if line.strip() == "#Waluta;":
            pending_currency = True
            continue
        elif pending_currency:
            currency = line.rstrip(";").strip()
            pending_currency = False
            logger.info("import: currency=%s", currency)
            continue

        if line.strip() == "#Numer rachunku;":
            pending_account = True
            continue
        elif pending_account:
            this_account_number = line.rstrip(";").strip()
            pending_account = False
            logger.info("import: this_account=%s", this_account_number)
            continue

        if not in_table and line.startswith("#Data ksi"):
            in_table = True
            logger.info("import: found table header at line=%d", total_lines)
            buf.write(line + "\n")
            continue

        if in_table:
            if line.startswith(";;;;;;#Saldo"):
                logger.info(
                    "import: end of table at line=%d (table_lines=%d)",
                    total_lines, table_lines
                )
                break

            # skip lines that are effectively empty
            if all(cell.strip() == "" for cell in line.split(";")):
                continue

            buf.write(line + "\n")
            table_lines += 1

            if table_lines % 500 == 0:
                logger.info("import: buffered %d tx rows (line=%d)", table_lines, total_lines)

    currency = currency or "UNKNOWN"

    table = buf.getvalue()
    if not table.strip():
        raise ValueError("No transaction table found (missing #Data księgowania header?).")

    df = pl.read_csv(
        table.encode("utf-8"),
        separator=";",
        has_header=True,
        infer_schema_length=1000,
        truncate_ragged_lines=True
    )

    def parse_amount(col: str) -> pl.Expr:
        return (
            pl.col(col)
            .cast(pl.Utf8)
            .str.replace_all(" ", "")
            .str.replace_all(",", ".")
            .cast(pl.Decimal(18, 2))
        )

    results_df_set = (
        df.rename(
            {
                "#Data operacji": "date",
                "#Opis operacji": "description",
                "#Tytuł": "title",
                "#Nadawca/Odbiorca": "other_account_name",
                "#Numer konta": "other_account_number",
                "#Kwota": "amount",
                '#Saldo po operacji': "amount_after_transaction",
            }
        )
        .with_columns(
            pl.col("date").str.strptime(pl.Date, "%Y-%m-%d", strict=True),

            pl.col("description")
            .cast(pl.Utf8)
            .str.strip_chars()
            .str.replace_all(r"\s+", " ")
            .str.replace_all(r"\"", "")
            .alias("description_clean"),

            pl.col("title")
            .cast(pl.Utf8)
            .str.strip_chars()
            .str.replace_all(r"\s+", " ")
            .str.replace_all(r"\"", "")
            .alias("title_clean"),

            pl.col("other_account_name")
            .cast(pl.Utf8)
            .str.strip_chars()
            .str.replace_all(r"\s+", " ")
            .str.replace_all(r"\"", "")
            .alias("other_account_name"),

            pl.col("other_account_number")
            .cast(pl.Utf8)
            .str.strip_chars()
            .str.strip_chars("'")
            .replace("", None),

            parse_amount("amount").alias("amount"),

            parse_amount("amount_after_transaction").alias("amount_after_transaction"),

            pl.lit(currency).alias("currency"),

            pl.lit(this_account_number).str.strip_chars().alias("this_account_number"),
        )
        .with_columns(
            pl.concat_str(
                [
                    pl.col("title_clean").replace("", None),
                    pl.col("description_clean").replace("", None),
                ],
                separator=" | ",
                ignore_nulls=True,
            )
            .str.replace_all(r"\s+", " ")
            .alias("description")
        )
        .select(
            "date",
            "description",
            "other_account_name",
            "other_account_number",
            "amount",
            "currency",
            "this_account_number",
        )
    )

    return [ParsedTx(**row, raw_payload=row) for row in results_df_set.to_dicts()]
