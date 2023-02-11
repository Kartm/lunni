from io import StringIO

import pandas as pd
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def home(request, *args, **kwargs):
    if request.method == "POST":
        csv_string_data = request.POST['file']
        string_io = StringIO(csv_string_data)
        df = pd.read_csv(string_io, skiprows=25, sep=';')

        print(df)

    return HttpResponse()
