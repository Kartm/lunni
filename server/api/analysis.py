import pandas as pd
import calendar


def analyseExportedCVS(file):
    df = file
    df.columns = df.columns.str.strip()

    # Convert 'date' column to datetime type
    df['date'] = pd.to_datetime(df['date'])

    # Extract month and year from 'date' column and get month name
    df['month'] = df['date'].dt.strftime('%B %Y')

    # Calculate total amount per category per month
    total_amount_per_category_per_month = df.groupby(['month', 'category_name'])['calculated_amount'].sum()

    # Convert the result to JSON
    json_data = total_amount_per_category_per_month.reset_index().to_json(orient='records')

    # Display the JSON data
    print(json_data)