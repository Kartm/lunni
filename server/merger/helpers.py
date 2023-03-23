from io import BytesIO

import pandas as pd


def file_to_entries(file: BytesIO):
    df = pd.read_csv(file, skiprows=25, sep=';', index_col=False, )

    # take only necessary rows
    df = df.iloc[:, :5]

    # rename headers
    df = df.rename(
        columns={
            '#Data operacji': 'Date',
            '#Opis operacji': 'Description',
            '#Rachunek': 'Account',
            '#Kategoria': 'Category',
            '#Kwota': 'Amount',
        }
    )

    # parse 'Amount' column
    # e.g. 7 921,39 PLN -> 7921.39
    # todo improve performance
    df['Amount'] = df['Amount'].apply(
        lambda amount:
        amount.replace("PLN", "")
        .replace(",", "")
        .replace(" ", "")
    ).astype(int)

    renamed_entries = df.rename(
        columns={
            'Date': 'date',
            'Description': 'description',
            'Account': 'account',
            'Category': 'category',
            'Amount': 'amount',
        }
    ).to_dict('records')

    return renamed_entries
