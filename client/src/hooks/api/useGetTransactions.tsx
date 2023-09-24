import { useQuery } from 'react-query';
import { getTransactions } from '../../api/merger';
import { message } from 'antd';
import { TableParams } from '../../components/organisms/EntryTable';
import { useMemo } from 'react';

const getUrlParams = (tableParams: TableParams) => {
    const entries: [string, string][] = [];

    if (tableParams.pagination?.current) {
        entries.push(['page', tableParams.pagination.current.toString()]);
    }

    if (tableParams.pagination?.pageSize) {
        entries.push(['page_size', tableParams.pagination.pageSize.toString()]);
    }

    if (tableParams.filters) {
        for (const [column, filterValues] of Object.entries(tableParams.filters)) {
            if (filterValues === null || filterValues.length === 0) {
                continue;
            }

            filterValues.forEach(filterValue => {
                if (typeof filterValue === 'boolean') {
                    if (!filterValue) {
                        entries.push(['uncategorized', 'true']);
                    }
                } else {
                    entries.push([column, filterValue.toString()]);
                }
            });
        }
    }

    return new URLSearchParams(entries);
};

export const useGetTransactions = (tableParams: TableParams) => {
    const urlParams = useMemo(() => getUrlParams(tableParams), [tableParams]);

    return useQuery({
        queryKey: [
            'get-transactions',
            tableParams],
        queryFn: () => getTransactions(urlParams),
        onError: (e) => message.error({ content: e?.toString() }),
    });
};
