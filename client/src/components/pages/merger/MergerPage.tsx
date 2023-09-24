import {DataType, EntryTable, TableParams} from '../../organisms/EntryTable';
import React, { useState } from 'react';
import {
	useGetTransactions,
	useMergeTransactions,
	useUpdateTransaction,
} from '../../../hooks/api';
import { TransactionMerger } from '../../molecules/TransactionMerger';
import { CategoryMatcherAdder } from '../../molecules/CategoryMatcherAdder';
import { Divider, Space } from 'antd';
import { TransactionPartial } from '../../../api/merger';
import { MergerPageActions } from './MergerPageActions';

export const MergerPage = () => {
	const [tableParams, setTableParams] = useState<TableParams>({});

	const { selection, setSelection, mergeTransactions } =
		useMergeTransactions();
	const [categoryAddRecord, setCategoryAddRecord] = useState<DataType>();
	const { mutate: updateTransaction } = useUpdateTransaction();

	const { data, isLoading: isGetTransactionsLoading } =
		useGetTransactions(tableParams);

	const handleMerge = (sourceId: number, targetId: number, amount: number) => {
		mergeTransactions({
			from_transaction: sourceId,
			to_transaction: targetId,
			amount,
		});
	};

	const onCategoryAdd = (record: DataType) => {
		setCategoryAddRecord(record);
	};

	const onRecordUpdate = (transactionPartial: TransactionPartial) => {
		updateTransaction(transactionPartial);
	};

	return (
		<>
			<CategoryMatcherAdder
				record={categoryAddRecord}
				onClose={() => setCategoryAddRecord(undefined)}
			/>

			<MergerPageActions />

			<Divider />

			<EntryTable
				isLoading={isGetTransactionsLoading}
				totalEntries={data?.count}
				data={data?.results || []}
				selection={selection}
				onSelectionChange={setSelection}
				onChange={(params) =>
					setTableParams(params)
				}
				onCategoryAdd={onCategoryAdd}
				onRecordUpdate={onRecordUpdate}
				mergeComponent={() => (
					<Space>
						<TransactionMerger
							mergeSelection={selection}
							data={data?.results || []}
							onMerge={handleMerge}
						/>
					</Space>
				)}
			/>
		</>
	);
};
