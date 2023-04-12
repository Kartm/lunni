export type TransactionCategory = {
  id: number;
  name: string;
  variant: "POS" | "NEG" | "IGN";
};

export type Transaction = {
  id: number;
  account: string;
  category: TransactionCategory | null;
  date: string;
  description: string;
  amount: number;
};
