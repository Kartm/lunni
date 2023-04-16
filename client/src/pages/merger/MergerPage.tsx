import { DataType, EntryTable } from "../../components/EntryTable";
import React, { useEffect, useState } from "react";
import { FileUpload } from "../../components/FileUpload";
import { useUploadFile } from "../../hooks/merger/useUploadFile";
import { useGetTransactions } from "../../hooks/merger/useGetTransactions";
import { MergeButton } from "../../components/MergeButton";
import { Key } from "antd/es/table/interface";
import { useMergeMutations } from "../../hooks/merger/useMergeTransactions";
import { RematchCategoriesButton } from "../../components/RematchCategoriesButton";
import { CategoryAddDrawer } from "../../components/CategoryAddDrawer";

export const MergerPage = () => {
  const [mergeSelection, setMergeSelection] = useState<Key[]>([]);
  const [pagination, setPagination] = useState<{
    page: number;
    pageSize: number;
  }>({ page: 1, pageSize: 50 });
  const mergeTransactions = useMergeMutations();
  const { isLoading: isUploadFileLoading, mutate } = useUploadFile();
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
  const onCategoryAdd = (record: DataType) => {
    setCategoryAddRecord(record);
  };

  useEffect(() => {
    mergeTransactions.isSuccess && setMergeSelection([]);
  }, [mergeTransactions.isSuccess]);

  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <FileUpload
          isUploading={isUploadFileLoading}
          onFileUpload={(fileUpload) => mutate(fileUpload)}
        />
      </div>
      <div style={{ marginBottom: 16 }}>
        <MergeButton
          mergeSelection={mergeSelection}
          data={data?.results || []}
          onMerge={handleMerge}
        />
      </div>
      <div style={{ marginBottom: 16 }}>
        <RematchCategoriesButton />
      </div>
      <CategoryAddDrawer
        record={categoryAddRecord}
        onClose={() => setCategoryAddRecord(undefined)}
      />

      <EntryTable
        isLoading={
          isGetTransactionsLoading ||
          isUploadFileLoading ||
          mergeTransactions.isLoading
        }
        totalEntries={data?.count}
        data={data?.results || []}
        mergeSelection={mergeSelection}
        onMergeSelectionChange={setMergeSelection}
        onPaginationChange={(page, pageSize) =>
          setPagination({ page, pageSize })
        }
        onCategoryAdd={onCategoryAdd}
      />
    </div>
  );
};
