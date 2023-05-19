import { useMutation, useQueryClient } from "react-query";
import {
  postMergeTransactions,
  TransactionMergeRequest,
} from "../../api/merger";
import { Key, useState } from "react";

export const useMergeTransactions = () => {
  const [mergeSelection, setMergeSelection] = useState<Key[]>([]);

  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationKey: "merge-mutations",
    mutationFn: (merge: TransactionMergeRequest) =>
      postMergeTransactions(merge),
    onSuccess: () => {
      setMergeSelection([]);
      queryClient.invalidateQueries({ queryKey: ["get-transactions"] });
    },
  });

  return {
    selection: mergeSelection,
    setSelection: setMergeSelection,
    isLoading: mutation.isLoading,
    mergeTransactions: mutation.mutate,
  };
};
