import { DataType } from '../../components/organisms/EntryTable';
import React, { useMemo } from 'react';
import { TransactionPartial } from '../../api/merger';
import { ColumnsType } from 'antd/lib/table';
import { EntryTableDescriptionCell } from '../../components/molecules/EntryTableDescriptionCell';
import { EntryTableCategoryCell } from '../../components/molecules/EntryTableCategoryCell';
import { EntryTableNoteCell } from '../../components/molecules/EntryTableNoteCell';
import { EntryTableAmountCell } from '../../components/molecules/EntryTableAmountCell';

type useEntryTableColumnsProps = {
	onCategoryAdd: (record: DataType) => void;
	onRecordUpdate: (transactionPartial: TransactionPartial) => void;
};

export const useEntryTableColumns = ({
	onCategoryAdd,
	onRecordUpdate,
}: useEntryTableColumnsProps): ColumnsType<DataType> =>
	useMemo(
		(): ColumnsType<DataType> => [
			{
				title: 'Date',
				dataIndex: 'date',
				key: 'date',
				width: 115,
			},
			{
				title: 'Description',
				dataIndex: 'description',
				key: 'description',
				ellipsis: true,
				render: (description: string) => (
					<EntryTableDescriptionCell description={description} />
				),
			},
			{
				title: 'Category',
				dataIndex: 'category',
				key: 'category',
				width: 140,
				ellipsis: true,
				render: (category: DataType['category'], record) => (
					<EntryTableCategoryCell
						category={category}
						onClickAdd={() => onCategoryAdd(record)}
					/>
				),
			},
			{
				title: 'Note',
				dataIndex: 'note',
				key: 'note',
				width: 150,
				render: (_, record) => (
					<EntryTableNoteCell
						defaultNote={record.note}
						onNoteChange={(note) => onRecordUpdate({ id: record.id, note })}
					/>
				),
			},
			{
				title: 'Account',
				dataIndex: 'account',
				key: 'account',
				width: 80,
				ellipsis: true,
			},
			{
				title: 'Amount',
				dataIndex: 'calculated_amount',
				key: 'amount',
				width: 150,
				align: 'right',
				render: (amount: number) => <EntryTableAmountCell amount={amount} />,
			},
		],
		[onCategoryAdd, onRecordUpdate]
	);
