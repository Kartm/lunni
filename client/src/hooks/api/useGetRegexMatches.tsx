import { useGetUnpaginatedTransactions } from './useGetUnpaginatedTransactions';

export const useGetRegexMatches = (regexExpression?: string) => {
    return useGetUnpaginatedTransactions({ searchRegex: regexExpression }, regexExpression !== undefined);
};
