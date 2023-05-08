import React, { useMemo } from "react";
import { Button, Table, Tag, Typography } from "antd";
import { Transaction } from "../../models/merger";
import { Key } from "antd/es/table/interface";
import { ColumnsType } from "antd/lib/table";

const { Text } = Typography;

export type DataType = Transaction & { key: Key; tags: string[] };

type EntryTableProps = {
  totalEntries?: number;
  isLoading?: boolean;
  data: Transaction[];
  mergeSelection: Key[];
  onMergeSelectionChange: (keys: Key[]) => void;
  onPaginationChange: (page: number, pageSize: number) => void;
  onCategoryAdd: (record: DataType) => void;
  summary: () => React.ReactNode;
};

export const EntryTable = ({
  isLoading,
  data,
  totalEntries,
  mergeSelection,
  onMergeSelectionChange,
  onPaginationChange,
  onCategoryAdd,
  summary,
}: EntryTableProps) => {
  const dataSource: DataType[] = useMemo(
    () =>
      data.map((transaction) => ({
        ...transaction,
        key: transaction.id,
        tags: getTags(transaction, mergeSelection),
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

  return (
    <Table
      loading={isLoading}
      dataSource={dataSource}
      columns={getColumns({ onCategoryAdd })}
      rowSelection={{
        type: "checkbox",
        hideSelectAll: true,
        onChange: (selectedRowKeys) => onMergeSelectionChange(selectedRowKeys),
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
        position: ["bottomRight"],
      }}
      scroll={{ x: 1200 }}
      summary={() =>
        summary ? (
          <Table.Summary fixed={"bottom"}>
            <Table.Summary.Row>
              <Table.Summary.Cell index={0} colSpan={2}></Table.Summary.Cell>
              <Table.Summary.Cell index={2} colSpan={8}>
                {summary()}
              </Table.Summary.Cell>
            </Table.Summary.Row>
          </Table.Summary>
        ) : null
      }
      sticky
    />
  );
};

const getTags = (transaction: Transaction, mergeSelection: React.Key[]) => {
  if (transaction.id === mergeSelection[0]) return ["from"];
  if (transaction.id === mergeSelection[1]) return ["to"];
  return [];
};

const isCheckboxDisabled = (
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

const getColumns = ({
  onCategoryAdd,
}: {
  onCategoryAdd: (record: DataType) => void;
}): ColumnsType<DataType> => [
  {
    title: "",
    key: "tags",
    dataIndex: "tags",
    width: 120,
    render: (tags: string[]) => (
      <span>
        {tags.map((tag) => {
          const color = { from: "green", to: "red" }[tag] || "white";

          return (
            <Tag color={color} key={tag}>
              {tag.toUpperCase()}
            </Tag>
          );
        })}
      </span>
    ),
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
