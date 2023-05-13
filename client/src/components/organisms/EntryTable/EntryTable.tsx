import React, { useMemo } from "react";
import { Table } from "antd";
import { Transaction } from "../../../models/merger";
import { Key } from "antd/es/table/interface";
import { ColumnsType } from "antd/lib/table";
import { TransactionPartial } from "../../../api/merger";
import { debounce } from "lodash";
import { EntryTableCategoryCell } from "../../molecules/EntryTableCategoryCell";
import { EntryTableAmountCell } from "../../molecules/EntryTableAmountCell";
import { EntryTableNoteCell } from "../../molecules/EntryTableNoteCell";
import { EntryTableDescriptionCell } from "../../molecules/EntryTableDescriptionCell";

export type DataType = Transaction & {
  key: Key;
  mergeComponent: () => React.ReactNode;
};

type EntryTableProps = {
  totalEntries?: number;
  isLoading?: boolean;
  data: Transaction[];
  mergeSelection: Key[];
  onMergeSelectionChange: (keys: Key[]) => void;
  onPaginationChange: (page: number, pageSize: number) => void;
  onCategoryAdd: (record: DataType) => void;
  onRecordUpdate: (transactionPartial: TransactionPartial) => void;
  mergeComponent: () => React.ReactNode;
};

export const EntryTable = ({
  isLoading,
  data,
  totalEntries,
  mergeSelection,
  onMergeSelectionChange,
  onPaginationChange,
  onCategoryAdd,
  onRecordUpdate,
  mergeComponent,
}: EntryTableProps) => {
  const dataSource: DataType[] = useMemo(
    () =>
      data.map((transaction) => ({
        ...transaction,
        key: transaction.id,
        mergeComponent,
      })),
    [data, mergeSelection]
  );

  const disabledRows = useMemo(() => {
    const selectedRows = dataSource.filter((d) =>
      mergeSelection.includes(d.key)
    );

    return new Set(
      dataSource.filter((record) =>
        isCheckboxDisabled(record, dataSource, selectedRows)
      )
    );
  }, [dataSource, mergeSelection]);

  const onRowSelectionChange = (selectedRowKeys: Key[]) => {
    const selectedRows = dataSource.filter((d) =>
      selectedRowKeys.includes(d.key)
    );

    if (selectedRows.length === 1 && selectedRows[0].amount <= 0) {
      // if unselected "FROM", prevent "TO" from becoming "FROM" and having negative amount
      onMergeSelectionChange([]);
    } else {
      onMergeSelectionChange(selectedRowKeys);
    }
  };

  const onRecordUpdateDebounced = debounce(onRecordUpdate, 250);

  return (
    <Table
      loading={isLoading}
      dataSource={dataSource}
      columns={getColumns({
        onCategoryAdd,
        onRecordUpdate: onRecordUpdateDebounced,
      })}
      rowSelection={{
        type: "checkbox",
        hideSelectAll: true,
        onChange: (selectedRowKeys) => onRowSelectionChange(selectedRowKeys),
        selectedRowKeys: mergeSelection,
        getCheckboxProps: (record) => ({
          disabled: disabledRows.has(record),
        }),
      }}
      pagination={{
        total: totalEntries,
        defaultPageSize: 50,
        showSizeChanger: true,
        pageSizeOptions: [50, 100, 500, 1000],
        onChange: onPaginationChange,
        position: ["topRight"],
      }}
      expandable={{
        showExpandColumn: false,
        expandedRowRender: (record) => <div>{record.mergeComponent()}</div>,
        expandedRowKeys: mergeSelection.length === 2 ? [mergeSelection[0]] : [],
      }}
    />
  );
};

const isCheckboxDisabled = (
  record: DataType,
  dataSource: DataType[],
  selectedRows: DataType[]
) => {
  switch (selectedRows.length) {
    case 0: {
      return record.amount <= 0;
    }
    case 1: {
      const selectedRow = selectedRows[0];

      if (selectedRow.key === record.key) {
        return false;
      }

      return record.amount * selectedRow.amount > 0;
    }
    default: {
      return !selectedRows.includes(record);
    }
  }
};

const getColumns = ({
  onCategoryAdd,
  onRecordUpdate,
}: {
  onCategoryAdd: (record: DataType) => void;
  onRecordUpdate: (transactionPartial: TransactionPartial) => void;
}): ColumnsType<DataType> => [
  {
    title: "Date",
    dataIndex: "date",
    key: "date",
    width: 115,
  },
  {
    title: "Description",
    dataIndex: "description",
    key: "description",
    ellipsis: true,
    render: (description: string) => (
      <EntryTableDescriptionCell description={description} />
    ),
  },
  {
    title: "Category",
    dataIndex: "category",
    key: "category",
    width: 140,
    ellipsis: true,
    render: (category: DataType["category"], record) => (
      <EntryTableCategoryCell
        category={category}
        onClickAdd={() => onCategoryAdd(record)}
      />
    ),
  },
  {
    title: "Note",
    dataIndex: "note",
    key: "note",
    width: 150,
    render: (_, record) => (
      <EntryTableNoteCell
        defaultNote={record.note}
        onNoteChange={(note) => onRecordUpdate({ id: record.id, note })}
      />
    ),
  },
  {
    title: "Account",
    dataIndex: "account",
    key: "account",
    width: 80,
    ellipsis: true,
  },
  {
    title: "Amount",
    dataIndex: "calculated_amount",
    key: "amount",
    width: 150,
    align: "right",
    render: (amount: number) => <EntryTableAmountCell amount={amount} />,
  },
];
