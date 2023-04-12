export type TransactionCategory = {
  id: number;
  name: string;
};

export type Transaction = {
  id: number;
  account: string;
  category: TransactionCategory | null;
  date: string;
  description: string;
  amount: number;
};
