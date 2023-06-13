from abc import abstractmethod, ABC
from io import BytesIO
from typing import TypedDict, List

import pandas as pd


class Entry(TypedDict):
    date: str
    description: str
    account: str
    amount: int


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
        return pd.read_csv(file, skiprows=25, sep=';', index_col=False, encoding='utf8')

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
        return pd.read_csv(file, skiprows=37, skipfooter=5, sep=';', index_col=False, encoding='cp1250')

    def _transform_dataframe(self, df: pd.DataFrame) -> List[Entry]:
        my_df = df
        my_df['#Opis operacji'] = my_df['#Opis operacji'].fillna('') + ' ' + my_df['#Tytuł'].fillna('')

        # add header for compatibility with Entry type
        my_df["Account"] = "Cel"

        # rename headers
        my_df = df.rename(
            columns={
                '#Data operacji': 'Date',
                '#Opis operacji': 'Description',
                '#Rachunek': 'Account',
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


PARSERS = [
    MBankCSVParser(),
    MBankSavingsCSVParser(),
    PKOCSVParser()
]
