from abc import abstractmethod, ABC
from io import BytesIO
from typing import TypedDict, List

import pandas as pd


class Entry(TypedDict):
    date: str
    description: str
    account: str
    amount: int


def get_header_index(header_prefix: str, file: BytesIO, encoding: str) -> int:
    # stores the whole uploaded file in memory. it's not a problem until we reach a certain file size
    file_lines = file.read().decode(encoding).split("\n")
    header_index = next(
        (i for i, line in enumerate(file_lines) if line.startswith(header_prefix)), None)
    file.seek(0)
    return header_index


class BaseCSVParser(ABC):
    def __init__(self, symbol: str, label: str):
        self.symbol = symbol
        self.label = label

    @abstractmethod
    def _read_csv(self, file: BytesIO) -> pd.DataFrame:
        pass

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
        super().__init__(symbol='mbank', label='mBank')

    def _read_csv(self, file: BytesIO) -> pd.DataFrame:
        encoding = 'utf8'
        header_prefix = '#Data operacji;#'
        header_index = get_header_index(header_prefix, file, encoding)
        return pd.read_csv(file, skiprows=header_index, sep=';', index_col=False, encoding=encoding)

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
        super().__init__(symbol='mbank-savings', label='mBank Cele')

    def _read_csv(self, file: BytesIO) -> pd.DataFrame:
        encoding = 'windows-1250'
        header_prefix = '#Data księgowania;#' # todo extract this to base class
        header_index = get_header_index(header_prefix, file, encoding)
        return pd.read_csv(file, skiprows=header_index, skipfooter=5, sep=';', index_col=False, encoding=encoding)

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
        super().__init__(symbol='pko', label='PKO')

    def _read_csv(self, file: BytesIO) -> pd.DataFrame:
        return pd.read_csv(file, sep=',', index_col=False, encoding='cp1250')

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
        super().__init__(symbol='ing', label='ING Bank Śląski')

    def _read_csv(self, file: BytesIO) -> pd.DataFrame:
        encoding = 'windows-1250'
        header_prefix = '"Data transakcji";"Data księgowania";'
        header_index = get_header_index(header_prefix, file, encoding)
        return pd.read_csv(file, skiprows=header_index, skipfooter=3, sep=';', index_col=False, encoding=encoding)

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
