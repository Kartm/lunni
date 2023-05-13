import { DataType, EntryTable } from "../../organisms/EntryTable";
import React, { useEffect, useState } from "react";
import { BankStatementUploadModal } from "../../molecules/BankStatementUploadModal";
import { useGetTransactions } from "../../../hooks/api/useGetTransactions";
import { MergeButton } from "../../molecules/MergeButton";
import { Key } from "antd/es/table/interface";
import { useMergeMutations } from "../../../hooks/api/useMergeTransactions";
import { RematchCategoriesButton } from "../../molecules/RematchCategoriesButton";
import { CategoryAddDrawer } from "../../molecules/CategoryAddDrawer";
import { Space } from "antd";
import { TransactionPartial } from "../../../api/merger";
import { useUpdateTransaction } from "../../../hooks/api/useUpdateTransaction";
import { ExportButton } from "../../molecules/ExportButton";

export const MergerPage = () => {
  const [mergeSelection, setMergeSelection] = useState<Key[]>([]);
  const [pagination, setPagination] = useState<{
    page: number;
    pageSize: number;
  }>({ page: 1, pageSize: 50 });
  const mergeTransactions = useMergeMutations();
  const { data, isLoading: isGetTransactionsLoading } = useGetTransactions(
    pagination.page,
    pagination.pageSize
  );

  const handleMerge = (sourceId: number, targetId: number, amount: number) => {
    mergeTransactions.mutate({
      from_transaction: sourceId,
      to_transaction: targetId,
      amount: amount * 1,
    });
  };

  const [categoryAddRecord, setCategoryAddRecord] = useState<DataType>();
  const { mutate: updateTransaction } = useUpdateTransaction();
  const onCategoryAdd = (record: DataType) => {
    setCategoryAddRecord(record);
  };

  const onRecordUpdate = (transactionPartial: TransactionPartial) => {
    updateTransaction(transactionPartial);
  };

  useEffect(() => {
    mergeTransactions.isSuccess && setMergeSelection([]);
  }, [mergeTransactions.isSuccess]);

  return (
    <div style={{ padding: "16px" }}>
      <CategoryAddDrawer
        record={categoryAddRecord}
        onClose={() => setCategoryAddRecord(undefined)}
      />

      <Space style={{ marginBottom: "16px" }}>
        <BankStatementUploadModal />

        <RematchCategoriesButton />

        <ExportButton />
      </Space>

      <EntryTable
        isLoading={isGetTransactionsLoading || mergeTransactions.isLoading}
        totalEntries={data?.count}
        data={data?.results || []}
        mergeSelection={mergeSelection}
        onMergeSelectionChange={setMergeSelection}
        onPaginationChange={(page, pageSize) =>
          setPagination({ page, pageSize })
        }
        onCategoryAdd={onCategoryAdd}
        onRecordUpdate={onRecordUpdate}
        mergeComponent={() => (
          <Space>
            <MergeButton
              mergeSelection={mergeSelection}
              data={data?.results || []}
              onMerge={handleMerge}
            />
          </Space>
        )}
      />
    </div>
  );
};
