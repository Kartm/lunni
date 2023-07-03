import {
	CategoryMatcher,
	CategoryStats,
	Transaction,
	TransactionCategory,
} from '../../models/merger';
import { Paginated } from '../../models/common/paginated.type';

export type UploadFileResponse = {
	new_entries: number;
};

export type UploadParsersResponse = Array<{ symbol: string; label: string }>;

export type TransactionResponse = Paginated<Transaction>;

export type TransactionMergeRequest = {
	from_transaction: number;
	to_transaction: number;
	amount: number;
};

export type CategoryStatsResponse = CategoryStats;

export type CategoriesResponse = Paginated<TransactionCategory>;

export type CategoryCreateRequest = Omit<TransactionCategory, 'id'>;

export type CategoryMatcherCreateRequest = Omit<
	CategoryMatcher,
	'id' | 'category'
> & {
	category_id: TransactionCategory['id'];
};

export type CategoryMatchersResponse = {
  results: CategoryMatcher[]
}

export type TransactionPartial = Pick<Transaction, 'id'> & Partial<Transaction>;

export type TransactionUpdateRequest = Omit<Partial<Transaction>, 'id'>;

export type TransactionUpdateResponse = Transaction;
