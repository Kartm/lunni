# Lunni - a tool for managing personal finance.

![Screenshot of the transaction table](./docs/screenshot.png)

If you frequently:

- ✅ make shared orders with friends
- ✅ utilize many bank accounts

then Lunni can help you to better organize and analyze your finance data.

# Try it out!

Feel free to import this [example PKO statement file](./docs/example_pko.csv).

# What Lunni can do:

1. Import .csv bank statements:
   - mBank
   - mBank savings (so-called "Cele")
   - PKO
2. Transaction Table
   - View transaction chronologically sorted in a table
3. Transaction Notes
   - Assign notes e.g. to document ambiguous transactions
4. Transaction Merging
   - Merge transactions to combine incoming money with expenses
   - Useful for handling shared orders with friends
5. Transaction Categories
   - Define transaction categories of type:
     - POSITIVE: Incomes
     - NEGATIVE: Expenses
     - IGNORE: Hidden in reports and the transaction table
6. Category Matchers
   - Automate categorization process by assigning categories to transactions using `regex`
7. Export to .csv
   - Export financial data to analyze it in external tools, for example Tableau, PowerBI, Google Data Studio

The format is the following:

| id  | date       | description | note | account       | category_name | amount | calculated_amount |
| --- | ---------- | ----------- | ---- | ------------- | ------------- | ------ | ----------------- |
| 1   | 2023-05-11 | Description |      | Prywatne 1234 | Maintenance   | -50    | -50               |

Where `calculated_amount` is the resulting amount after merging transactions.

# Future plans:

- Gradually add unit tests to cover newly found bugs
