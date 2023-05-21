import { DataType, EntryTable } from "../../organisms/EntryTable";
import React, { useState } from "react";
import { BankStatementUploadModal } from "../../molecules/BankStatementUploadModal";
import {
  useGetTransactions,
  useMergeTransactions,
  useUpdateTransaction,
} from "../../../hooks/api";
import { TransactionMerger } from "../../molecules/TransactionMerger";
import { RematchCategoriesButton } from "../../molecules/RematchCategoriesButton";
import { CategoryMatcherAdder } from "../../molecules/CategoryMatcherAdder";
import { Divider, Space } from "antd";
import { TransactionPartial } from "../../../api/merger";
import { ExportButton } from "../../molecules/ExportButton";
import { usePagination } from "../../../hooks/common/usePagination";

export const MergerPage = () => {
  const { pagination, setPagination } = usePagination();

  const { selection, setSelection, isLoading, mergeTransactions } =
    useMergeTransactions();
  const [categoryAddRecord, setCategoryAddRecord] = useState<DataType>();
  const { mutate: updateTransaction } = useUpdateTransaction();

  const { data, isLoading: isGetTransactionsLoading } =
    useGetTransactions(pagination);

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

      <Space>
        <BankStatementUploadModal />

        <RematchCategoriesButton />

        <ExportButton />
      </Space>

      <Divider />

      <EntryTable
        isLoading={isGetTransactionsLoading || isLoading}
        totalEntries={data?.count}
        data={data?.results || []}
        selection={selection}
        onSelectionChange={setSelection}
        onPaginationChange={(page, pageSize) =>
          setPagination({ page, pageSize })
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
