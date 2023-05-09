import React, { useMemo } from "react";
import { Button, Table, Typography } from "antd";
import { Transaction } from "../../models/merger";
import { Key } from "antd/es/table/interface";
import { ColumnsType } from "antd/lib/table";
import { PlusCircleOutlined } from "@ant-design/icons";

const { Text } = Typography;

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

  const checkboxToDisabled = useMemo(() => {
    const selectedRows = dataSource.filter((d) =>
      mergeSelection.includes(d.key)
    );

    return new Map(
      dataSource.map((record) => [
        record,
        isCheckboxDisabled(record, dataSource, selectedRows),
      ])
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

  return (
    <Table
      loading={isLoading}
      dataSource={dataSource}
      columns={getColumns({ onCategoryAdd })}
      rowSelection={{
        type: "checkbox",
        hideSelectAll: true,
        onChange: (selectedRowKeys) => onRowSelectionChange(selectedRowKeys),
        selectedRowKeys: mergeSelection,
        getCheckboxProps: (record) => ({
          disabled: checkboxToDisabled.get(record),
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
}: {
  onCategoryAdd: (record: DataType) => void;
}): ColumnsType<DataType> => [
  {
    title: "Date",
    dataIndex: "date",
    key: "date",
    width: 120,
  },
  {
    title: "Description",
    dataIndex: "description",
    key: "description",
    ellipsis: true,
    render: (description: string) => (
      <span title={description}>{description}</span>
    ),
  },
  {
    title: "Category",
    dataIndex: "category",
    key: "category",
    width: 150,
    render: (category: DataType["category"], record) => (
      <Text
        type={
          category?.variant === "POS"
            ? "success"
            : category?.variant === "NEG"
            ? "danger"
            : "secondary"
        }
      >
        {category?.name || (
          <Button
            icon={<PlusCircleOutlined />}
            size={"small"}
            type={"ghost"}
            title={"Category is missing"}
            onClick={() => onCategoryAdd(record)}
          />
        )}
      </Text>
    ),
  },
  {
    title: "Account",
    dataIndex: "account",
    key: "account",
    width: 200,
  },
  {
    title: "Amount",
    dataIndex: "calculated_amount",
    key: "amount",
    width: 150,
    align: "right",
    render: (amount: number) => (
      <Text type={amount > 0 ? "success" : "danger"}>
        {`${(amount / 100).toFixed(2)} PLN`}
      </Text>
    ),
  },
];
