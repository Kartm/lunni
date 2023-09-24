import { useQuery } from 'react-query';
import { getRegexMatches } from '../../api/merger';
import { message } from 'antd';

export const useGetRegexMatches = (regexExpression?: string) => {
    return useQuery({
        enabled: regexExpression !== undefined,
        queryKey: ['get-regex-matches', regexExpression],
        queryFn: () => getRegexMatches(regexExpression!),
        onError: (e) => message.error({ content: e?.toString() }),
    });
};
