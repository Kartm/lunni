import { useQuery } from "react-query";
import { getCategories, getTransactions } from "../../api/merger";
import { message } from "antd";

export const useCategoryList = () => {
  return useQuery({
    queryKey: ["get-categories"],
    queryFn: () => getCategories(),
  });
};
