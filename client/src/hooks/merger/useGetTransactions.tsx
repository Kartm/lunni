import { useQuery } from "react-query";
import { getTransactions } from "../../api/merger";
import { message } from "antd";

export const useGetTransactions = () => {
  return useQuery({
    queryKey: "get-transactions",
    queryFn: () => getTransactions(),
    onError: (e) => message.error({ content: e?.toString() }),
  });
};
