import { useQuery } from 'react-query';
import { getUnpaginatedTransactions } from '../../api/merger';
import { message } from 'antd';
import { TableParams } from '../../components/organisms/EntryTable';
import { useUrlQueryFromTableParams } from './useUrlQueryFromTableParams';

export const useGetUnpaginatedTransactions = (tableParams: TableParams, enabled = true) => {
    const urlParams = useUrlQueryFromTableParams(tableParams);

    return useQuery({
        enabled,
        queryKey: [
            'get-transactions',
            tableParams],
        queryFn: () => getUnpaginatedTransactions(urlParams),
        onError: (e) => message.error({ content: e?.toString() }),
        keepPreviousData: true,
    });
};
