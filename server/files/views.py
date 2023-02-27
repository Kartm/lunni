import pandas as pd
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


@require_POST
@csrf_exempt
def home(request, *args, **kwargs):
    in_memory_file = request.FILES.get('file')
    bytes_io = in_memory_file.file
    df = pd.read_csv(bytes_io, skiprows=25, sep=';', index_col=False, parse_dates=['#Data operacji'])

    # take only necessary columns
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
            .replace(",", ".")
            .replace(" ", "")
    ).astype(float)

    print(df.info())

    return HttpResponse()
