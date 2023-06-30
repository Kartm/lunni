from abc import abstractmethod, ABC
from io import BytesIO
from typing import TypedDict, List, Tuple

import pandas as pd


class Entry(TypedDict):
    date: str
    description: str
    account: str
    amount: int


def get_start_stop_indexes(header_prefix: str, file: BytesIO, encoding: str) -> Tuple[int, int]:
    # stores the whole uploaded file in memory. it's not a problem until we reach a certain file size
    file_lines = file.read().decode(encoding).split("\n")
    start_index = None
    stop_index = None
    for i, line in enumerate(file_lines):
        if line.startswith(header_prefix):
            start_index = i

        # strip to interpret '\r' as empty lines
        elif start_index is not None and line.strip() == '':
            stop_index = i - 1
            break

    file.seek(0)
    return start_index, stop_index


class BaseCSVParser(ABC):
    def __init__(self, symbol: str, label: str, encoding: str, header_prefix: str, column_separator: str):
        self.symbol = symbol
        self.label = label
        self.encoding = encoding
        self.header_prefix = header_prefix
        self.column_separator = column_separator

    def _read_csv(self, file: BytesIO) -> pd.DataFrame:
        start_index, stop_index = get_start_stop_indexes(self.header_prefix, file, self.encoding)
        rows_to_read = stop_index - start_index
        return pd.read_csv(file, skiprows=start_index, skip_blank_lines=False, nrows=rows_to_read,
                           sep=self.column_separator, index_col=False, encoding=self.encoding)

    @abstractmethod
    def _transform_dataframe(self, df: pd.DataFrame) -> List[Entry]:
        pass

    def parse_csv_file(self, file: BytesIO) -> List[Entry]:
        df = self._read_csv(file)
        parsed_entries = self._transform_dataframe(df)

        parsed_entries = parsed_entries.drop_duplicates()

        parsed_entries = parsed_entries.rename(
            columns={
                'Date': 'date',
                'Description': 'description',
                'Account': 'account',
                'Amount': 'amount',
            }
        ).to_dict('records')

        return parsed_entries


class MBankCSVParser(BaseCSVParser):
    def __init__(self):
        super().__init__(symbol='mbank', label='mBank', encoding='utf8', header_prefix='#Data operacji;#',
                         column_separator=';')

    def _transform_dataframe(self, df: pd.DataFrame) -> List[Entry]:
        # take only necessary columns
        my_df = df.iloc[:, :5]

        # rename headers
        my_df = my_df.rename(
            columns={
                '#Data operacji': 'Date',
                '#Opis operacji': 'Description',
                '#Rachunek': 'Account',
                '#Kwota': 'Amount',
            }
        )

        # e.g. 7 921,39 PLN -> 7921.39
        my_df['Amount'] = my_df['Amount'].apply(
            lambda amount:
            amount.replace("PLN", "")
            .replace(",", "")
            .replace(" ", "")
        ).astype(int)

        my_df['Description'] = my_df['Description'].apply(
            lambda description:
            " ".join(description.split())
        ).astype(str)

        return my_df


class MBankSavingsCSVParser(BaseCSVParser):
    def __init__(self):
        super().__init__(symbol='mbank-savings', label='mBank Cele', encoding='windows-1250',
                         header_prefix='#Data księgowania;#', column_separator=';')

    def _transform_dataframe(self, df: pd.DataFrame) -> List[Entry]:
        my_df = df

        # add header for compatibility with Entry type
        my_df["Account"] = "Cel"

        # rename headers
        my_df = df.rename(
            columns={
                '#Data operacji': 'Date',
                '#Opis operacji': 'Description',
                '#Kwota': 'Amount',
            }
        )

        # e.g. 7 921,39 -> 7921.39
        my_df['Amount'] = my_df['Amount'].apply(
            lambda amount:
            str(amount).replace(",", "")
            .replace(" ", "")
        ).astype(int)

        my_df['Description'] = my_df['Description'].apply(
            lambda description:
            " ".join(description.split())
        ).astype(str)

        return my_df


class PKOCSVParser(BaseCSVParser):
    def __init__(self):
        super().__init__(symbol='pko', label='PKO', encoding='windows-1250', header_prefix='"Data operacji"',
                         column_separator=',')

    def _transform_dataframe(self, df: pd.DataFrame) -> List[Entry]:
        # rename headers
        my_df = df.rename(
            columns={
                'Data operacji': 'Date',
                'Kwota': 'Amount',
            }
        )

        # next-to-last column contains real transfer title, but sometimes it's missing
        # falls back to 'Opis transakcji', which typically stores sender's account number but it's better than nothing
        col = my_df.columns[-2]
        my_df['Description'] = my_df[col].fillna(my_df['Opis transakcji'])

        # add header for compatibility with Entry type
        my_df["Account"] = "PKO"

        # e.g. +20.10 -> 20.10, -10.00 -> -10
        my_df['Amount'] = my_df['Amount'].apply(
            lambda amount:
            amount * 100
        ).astype(int)

        my_df['Description'] = my_df['Description'].apply(
            lambda description:
            " ".join(description.split())
        ).astype(str)

        return my_df


class INGCSVParser(BaseCSVParser):
    def __init__(self):
        super().__init__(symbol='ing', label='ING Bank Śląski', encoding='windows-1250',
                         header_prefix='"Data transakcji";"Data księgowania";', column_separator=';')

    def _transform_dataframe(self, df: pd.DataFrame) -> List[Entry]:
        my_df = df

        # rename headers
        my_df = my_df.rename(
            columns={
                'Data transakcji': 'Date',
                'Konto': 'Account',
            }
        )

        my_df['Description'] = my_df['Dane kontrahenta'].fillna('') + ' ' + my_df['Tytuł'].fillna('')
        my_df['Amount'] = my_df['Kwota transakcji (waluta rachunku)'].fillna('') + my_df[
            'Kwota blokady/zwolnienie blokady'].fillna('') + my_df['Kwota płatności w walucie'].fillna('')

        # e.g. 7 921,39 -> 7921.39
        my_df['Amount'] = my_df['Amount'].apply(
            lambda amount:
            str(amount).replace(",", "")
            .replace(" ", "")
        ).astype(int)

        my_df['Description'] = my_df['Description'].apply(
            lambda description:
            " ".join(description.split())
        ).astype(str)

        return my_df


PARSERS = [
    MBankCSVParser(),
    MBankSavingsCSVParser(),
    PKOCSVParser(),
    INGCSVParser()
]
