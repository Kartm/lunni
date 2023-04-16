import { useQuery } from "react-query";
import { getRegexMatches, getTransactions } from "../../api/merger";
import { message } from "antd";

export const useGetRegexMatches = (regexExpression: string) => {
  return useQuery({
    queryKey: ["get-regex-matches", regexExpression],
    queryFn: () => getRegexMatches(regexExpression),
    onError: (e) => message.error({ content: e?.toString() }),
  });
};
