import { useQuery } from 'react-query';
import { getTransactions } from '../../api/merger';
import { message } from 'antd';
import { TableParams } from '../../components/organisms/EntryTable';
import { useUrlQueryFromTableParams } from './useUrlQueryFromTableParams';

export const useGetTransactions = (tableParams: TableParams) => {
    const urlParams = useUrlQueryFromTableParams(tableParams);

    return useQuery({
        queryKey: [
            'get-transactions',
            tableParams],
        queryFn: () => getTransactions(urlParams),
        onError: (e) => message.error({ content: e?.toString() }),
    });
};
