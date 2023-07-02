import { useQuery } from "react-query";
import { getRegexMatches, getTransactions } from "../../api/merger";
import { message } from "antd";

export const useGetRegexMatches = (regexExpression?: string) => {

  //Enable search for values containing regex special character *
  const parseSpecialChar = (value: string) => {
    return value.replaceAll("*", "[*]")
  }

  if(regexExpression){
    regexExpression = parseSpecialChar(regexExpression)
  }

  return useQuery({
    enabled: regexExpression !== undefined,
    queryKey: ["get-regex-matches", regexExpression],
    queryFn: () => getRegexMatches(regexExpression!!),
    onError: (e) => message.error({ content: e?.toString() }),
  });
};
