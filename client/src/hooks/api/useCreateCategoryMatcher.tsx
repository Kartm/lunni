import { useMutation, useQuery, useQueryClient } from "react-query";
import {
  CategoryCreateRequest,
  CategoryMatcherCreateRequest,
  createCategory,
  createCategoryMatcher,
  getCategories,
  getTransactions,
  postMergeTransactions,
  TransactionMergeRequest,
} from "../../api/merger";
import { message } from "antd";
import { useRematchCategories } from "./useRematchCategories";

export const useCreateCategoryMatcher = () => {
  const queryClient = useQueryClient();

  const { mutate: rematchCategories } = useRematchCategories();

  return useMutation({
    mutationKey: "create-category-matcher",
    mutationFn: (matcher: CategoryMatcherCreateRequest) =>
      createCategoryMatcher(matcher),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["get-category-matchers"] });
      rematchCategories();
    },
  });
};
