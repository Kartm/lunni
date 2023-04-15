import React, { useMemo } from "react";
import { Table, Typography } from "antd";
import { Transaction } from "../../models/merger";
import { Key } from "antd/es/table/interface";
import styled from "styled-components";
import { ColumnsType } from "antd/lib/table";

const { Text } = Typography;

const columns: ColumnsType<DataType> = [
  {
    title: "Id",
    dataIndex: "id",
    key: "id",
    width: 80,
  },
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
    render: (category: DataType["category"]) => (
      <Text
        type={
          category?.variant === "POS"
            ? "success"
            : category?.variant === "NEG"
            ? "danger"
            : "secondary"
        }
      >
        {category?.name || "(none)"}
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
    dataIndex: "amount",
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

type EntryTableProps = {
  totalEntries?: number;
  isLoading?: boolean;
  data: Transaction[];
  mergeSelection: Key[];
  onMergeSelectionChange: (keys: Key[]) => void;
  onPaginationChange: (page: number, pageSize: number) => void;
};

type DataType = Transaction & { key: Key };

const isRowDisabled = (
  record: DataType,
  dataSource: DataType[],
  selectedRowKeys: Key[]
) => {
  switch (selectedRowKeys.length) {
    case 0: {
      return false;
    }
    case 1: {
      const selectedRow = dataSource.find((d) => d.key === selectedRowKeys[0])!;

      if (selectedRow.key === record.key) {
        return false;
      }

      return record.amount * selectedRow.amount > 0;
    }
    default: {
      return !selectedRowKeys.includes(record.key);
    }
  }
};

const MyTable: typeof Table = styled(Table)`
  .disabled-row {
    color: #9a9a9a;
    pointer-events: none;
  }
`;

export const EntryTable = ({
  isLoading,
  data,
  totalEntries,
  mergeSelection,
  onMergeSelectionChange,
  onPaginationChange,
}: EntryTableProps) => {
  const dataSource: DataType[] = useMemo(
    () => data.map((d) => ({ ...d, key: d.id })),
    [data]
  );

  return (
    <MyTable
      loading={isLoading}
      dataSource={dataSource}
      columns={columns}
      rowClassName={(record) =>
        isRowDisabled(record, dataSource, mergeSelection) ? "disabled-row" : ""
      }
      rowSelection={{
        type: "checkbox",
        hideSelectAll: true,
        onChange: (selectedRowKeys) => onMergeSelectionChange(selectedRowKeys),
        selectedRowKeys: mergeSelection,
        getCheckboxProps: (record) => ({
          disabled: isRowDisabled(record, dataSource, mergeSelection),
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
    />
  );
};
