import { useMutation, useQueryClient } from "react-query";
import {
  RemoveCategoryRequest,
  removeCategory,
} from "../../api/merger";

export const useRemoveCategory = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationKey: "remove-category",
    mutationFn: (data: RemoveCategoryRequest) => removeCategory(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["get-categories"] });
    },
  });
};
