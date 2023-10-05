import { TableParams } from '../../components/organisms/EntryTable';
import { Key, useMemo } from 'react';



export const useUrlQueryFromTableParams = (tableParams: TableParams) => {
    const entries: [string, string][] = [];

    if (tableParams.pagination?.current) {
        entries.push(['page', tableParams.pagination.current.toString()]);
    }

    if (tableParams.pagination?.pageSize) {
        entries.push(['page_size', tableParams.pagination.pageSize.toString()]);
    }

    if (tableParams.customFilters?.date) {
        entries.push(['date_after', tableParams.customFilters.date.after]);
        entries.push(['date_before', tableParams.customFilters.date.before]);
    }

    if (tableParams.customFilters?.categories) {
        for (const category of tableParams.customFilters.categories) {
            if (category === null) {
                entries.push(['uncategorized', 'true']);
            } else {
                entries.push(['category', category]);
            }
        }
    }

    if (tableParams.sorter?.field) {
        const columns: Key[] = Array.isArray(tableParams.sorter.field) ? tableParams.sorter.field : [tableParams.sorter.field];

        for (let column of columns) {
            if (tableParams.sorter.order === 'descend') {
                column = `-${column}`;
            }

            entries.push(['ordering', column.toString()]);
        }
    }

    if (tableParams?.searchRegex) {
        entries.push(['search', tableParams.searchRegex]);
    }

    return useMemo(() => new URLSearchParams(entries), [tableParams]);
};
