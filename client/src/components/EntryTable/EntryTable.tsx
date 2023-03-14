import React, { useEffect, useState } from "react";
import { Table, Tooltip, Typography } from "antd";
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
      <Tooltip title={description}>{description}</Tooltip>
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
  isLoading?: boolean;
  data: Transaction[];
  mergeSelection: Key[];
  onMergeSelectionChange: (keys: Key[]) => void;
};

type DataType = Transaction & { key: Key };

const isRowDisabled = (
  record: DataType,
  dataSource: DataType[],
  selectedRowKeys: Key[]
) => {
  const already2Selected =
    !selectedRowKeys.includes(record.key) && selectedRowKeys.length >= 2;

  if (already2Selected) {
    return true;
  }

  if (selectedRowKeys.length === 1) {
    const selectedRow = dataSource.find((d) => d.key === selectedRowKeys[0]);

    if (selectedRow) {
      if (selectedRow.key !== record.key) {
        const bothSame = record.amount * selectedRow.amount > 0;

        if (bothSame) {
          return true;
        }
      }
    }
  }

  return false;
};

const MyTable: typeof Table = styled(Table)`
  .disabled-row {
    //opacity: 0.25;
    color: #9a9a9a;
    //pointer-events: none;
    background-color: #cbcbcb;
  }
`;

export const EntryTable = ({
  isLoading,
  data,
  mergeSelection,
  onMergeSelectionChange,
}: EntryTableProps) => {
  const dataSource: DataType[] = data.map((d) => ({ ...d, key: d.id }));

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
      pagination={{ pageSize: 50 }}
    />
  );
};
