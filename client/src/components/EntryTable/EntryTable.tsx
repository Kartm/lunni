import React, { useMemo } from "react";
import { Button, Table, Typography } from "antd";
import { Transaction } from "../../models/merger";
import { Key } from "antd/es/table/interface";
import styled from "styled-components";
import { ColumnsType } from "antd/lib/table";

const { Text } = Typography;

const getColumns = ({
  onCategoryAdd,
}: {
  onCategoryAdd: (record: DataType) => void;
}): ColumnsType<DataType> => [
  // {
  //   title: "Id",
  //   dataIndex: "id",
  //   key: "id",
  //   width: 80,
  // },
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
          <>
            (none)<Button onClick={() => onCategoryAdd(record)}>add</Button>
          </>
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

export type DataType = Transaction & { key: Key };

type EntryTableProps = {
  totalEntries?: number;
  isLoading?: boolean;
  data: Transaction[];
  mergeSelection: Key[];
  onMergeSelectionChange: (keys: Key[]) => void;
  onPaginationChange: (page: number, pageSize: number) => void;
  onCategoryAdd: (record: DataType) => void;
};

const isRowDisabled = (
  record: DataType,
  dataSource: DataType[],
  selectedRows: DataType[]
) => {
  switch (selectedRows.length) {
    case 0: {
      return false;
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
  onCategoryAdd,
}: EntryTableProps) => {
  const dataSource: DataType[] = useMemo(
    () => data.map((d) => ({ ...d, key: d.id })),
    [data]
  );

  const rowDisabled = useMemo(() => {
    const selectedRows = dataSource.filter((d) =>
      mergeSelection.includes(d.key)
    );

    return new Map(
      dataSource.map((record) => [
        record,
        isRowDisabled(record, dataSource, selectedRows),
      ])
    );
  }, [dataSource, mergeSelection]);

  return (
    <MyTable
      loading={isLoading}
      dataSource={dataSource}
      columns={getColumns({ onCategoryAdd })}
      rowClassName={(record) => (rowDisabled.get(record) ? "disabled-row" : "")}
      rowSelection={{
        type: "checkbox",
        hideSelectAll: true,
        onChange: (selectedRowKeys) => onMergeSelectionChange(selectedRowKeys),
        selectedRowKeys: mergeSelection,
        getCheckboxProps: (record) => ({
          disabled: rowDisabled.get(record),
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
