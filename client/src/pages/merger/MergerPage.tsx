import { EntryTable } from "../../components/EntryTable";
import React, { useEffect, useState } from "react";
import { FileUpload } from "../../components/FileUpload/FileUpload";
import { useUploadFile } from "../../hooks/merger/useUploadFile";
import { useGetTransactions } from "../../hooks/merger/useGetTransactions";
import { MergeButton } from "../../components/MergeButton";
import { Key } from "antd/es/table/interface";
import { useMergeMutations } from "../../hooks/merger/useMergeTransactions";

export const MergerPage = () => {
  const { isLoading: isUploadFileLoading, mutate } = useUploadFile();
  const { data, isLoading: isGetTransactionsLoading } = useGetTransactions();
  const [mergeSelection, setMergeSelection] = useState<Key[]>([]);
  const mergeTransactions = useMergeMutations();

  const handleMerge = (sourceId: number, targetId: number, amount: number) => {
    mergeTransactions.mutate({
      from_transaction: sourceId,
      to_transaction: targetId,
      amount: amount * 1,
    });
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

      <EntryTable
        isLoading={
          isGetTransactionsLoading ||
          isUploadFileLoading ||
          mergeTransactions.isLoading
        }
        data={data?.results || []}
        mergeSelection={mergeSelection}
        onMergeSelectionChange={setMergeSelection}
      />
    </div>
  );
};
