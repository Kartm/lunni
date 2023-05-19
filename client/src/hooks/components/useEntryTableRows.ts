import { DataType } from "../../components/organisms/EntryTable";
import { useCallback, useMemo } from "react";
import { Key } from "antd/es/table/interface";
import { Transaction } from "../../models/merger";

const isCheckboxDisabled = (
  record: DataType,
  dataSource: DataType[],
  selectedRows: Set<DataType>
) => {
  switch (selectedRows.size) {
    case 0: {
      return record.amount <= 0;
    }
    case 1: {
      const [selectedRow] = selectedRows;

      if (selectedRow.key === record.key) {
        return false;
      }

      return record.amount * selectedRow.amount > 0;
    }
    default: {
      return !selectedRows.has(record);
    }
  }
};

type useEntryTableRowsProps = {
  data: Transaction[];
  selection: React.Key[];
  onSelectionChange: (keys: Key[]) => void;
};

export const useEntryTableRows = ({
  data,
  selection,
  onSelectionChange,
}: useEntryTableRowsProps) => {
  const { dataSource, disabledRows } = useMemo(() => {
    const dataSource: DataType[] = data.map((transaction) => ({
      ...transaction,
      key: transaction.id,
    }));

    const selectedRows = new Set(
      dataSource.filter((d) => selection.includes(d.key))
    );

    const disabledRows = new Set(
      dataSource.filter((record) =>
        isCheckboxDisabled(record, dataSource, selectedRows)
      )
    );

    return { dataSource, disabledRows };
  }, [data, selection]);

  const onRowSelectionChange = useCallback(
    (selectedRowKeys: Key[]) => {
      const selectedRows = dataSource.filter((d) =>
        selectedRowKeys.includes(d.key)
      );

      if (selectedRows.length === 1 && selectedRows[0].amount <= 0) {
        // if unselected "FROM", prevent "TO" from becoming "FROM" and having negative amount
        onSelectionChange([]);
      } else {
        onSelectionChange(selectedRowKeys);
      }
    },
    [dataSource, onSelectionChange]
  );

  return { dataSource, disabledRows, onRowSelectionChange };
};
