import { useMutation, useQueryClient } from "react-query";
import {
  postMergeTransactions,
  postRematchCategories,
  TransactionMergeRequest,
  uploadFile,
} from "../../api/merger";
import { RcFile } from "antd/lib/upload";

export const useRematchCategories = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationKey: "rematch-categories",
    mutationFn: () => postRematchCategories(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["get-transactions"] });
    },
  });
};
