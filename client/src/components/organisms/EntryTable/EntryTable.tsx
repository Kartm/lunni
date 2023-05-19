import React from "react";
import { Table } from "antd";
import { Transaction } from "../../../models/merger";
import { Key } from "antd/es/table/interface";
import { TransactionPartial } from "../../../api/merger";
import { debounce } from "lodash";
import { useEntryTableRows } from "../../../hooks/components";
import { useEntryTableColumns } from "../../../hooks/components";

export type DataType = Transaction & {
  key: Key;
};

type EntryTableProps = {
  totalEntries?: number;
  isLoading?: boolean;
  data: Transaction[];
  selection: Key[];
  onSelectionChange: (keys: Key[]) => void;
  onPaginationChange: (page: number, pageSize: number) => void;
  onCategoryAdd: (record: DataType) => void;
  onRecordUpdate: (transactionPartial: TransactionPartial) => void;
  mergeComponent: ({ record }: { record: DataType }) => React.ReactNode;
};

export const EntryTable = ({
  isLoading,
  data,
  totalEntries,
  selection,
  onSelectionChange,
  onPaginationChange,
  onCategoryAdd,
  onRecordUpdate,
  mergeComponent,
}: EntryTableProps) => {
  const { dataSource, disabledRows, onRowSelectionChange } = useEntryTableRows({
    data,
    selection,
    onSelectionChange,
  });

  const onRecordUpdateDebounced = debounce(onRecordUpdate, 250);
  const columns = useEntryTableColumns({
    onCategoryAdd,
    onRecordUpdate: onRecordUpdateDebounced,
  });

  return (
    <Table
      loading={isLoading}
      dataSource={dataSource}
      columns={columns}
      rowSelection={{
        type: "checkbox",
        hideSelectAll: true,
        onChange: (selectedRowKeys) => onRowSelectionChange(selectedRowKeys),
        selectedRowKeys: selection,
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
        expandedRowRender: (record) => <div>{mergeComponent({ record })}</div>,
        expandedRowKeys: selection.length === 2 ? [selection[0]] : [],
      }}
    />
  );
};
