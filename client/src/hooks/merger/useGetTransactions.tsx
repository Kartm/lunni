import { useQuery } from "react-query";
import { getTransactions } from "../../api/merger";
import { message } from "antd";

export const useGetTransactions = (page: number, pageSize: number) => {
  return useQuery({
    queryKey: ["get-transactions", page, pageSize],
    queryFn: () => getTransactions(page, pageSize),
    onError: (e) => message.error({ content: e?.toString() }),
  });
};
