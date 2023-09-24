import { TableParams } from '../../components/organisms/EntryTable';
import { useMemo } from 'react';

export const useUrlQueryFromTableParams = (tableParams: TableParams) => {
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

    return useMemo(() => new URLSearchParams(entries), [tableParams]);
};
