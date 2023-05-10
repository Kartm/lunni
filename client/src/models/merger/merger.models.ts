export type TransactionCategory = {
  id: number;
  name: string;
  variant: "POS" | "NEG" | "IGN";
};

export type Transaction = {
  id: number;
  account: string;

  note: string;
  calculated_amount: string; // transaction merges taken into account
  category: TransactionCategory | null;
  date: string;
  description: string;
  amount: number;
};

export type CategoryStats = Array<{
  categoryName: string | null;
  totalCount: number;
}>;

export type CategoryMatcher = {
  id: number;
  regex_expression: string;
  category: TransactionCategory;
};
