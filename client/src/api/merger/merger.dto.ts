import { CategoryStats, Transaction } from "../../models/merger";
import { Paginated } from "../../models/common/paginated.type";

export type UploadFileResponse = {};

export type TransactionResponse = Paginated<Transaction>;

export type TransactionMergeRequest = {
  from_transaction: number;
  to_transaction: number;
  amount: number;
};

export type CategoryStatsResponse = CategoryStats;
