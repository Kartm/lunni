import { useMutation, useQuery, useQueryClient } from "react-query";
import {
  CategoryCreateRequest,
  createCategory,
  getCategories,
  getTransactions,
  postMergeTransactions,
  TransactionMergeRequest,
} from "../../api/merger";
import { message } from "antd";

export const useCreateCategory = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationKey: "create-category",
    mutationFn: (category: CategoryCreateRequest) => createCategory(category),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["get-categories"] });
    },
  });
};
