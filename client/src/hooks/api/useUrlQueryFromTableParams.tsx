import { TableParams } from '../../components/organisms/EntryTable';
import { Key, useMemo } from 'react';



export const useUrlQueryFromTableParams = (tableParams: TableParams) => {
    const entries: [string, string][] = [];

    if (tableParams.pagination) {
        entries.push(['page', tableParams.pagination.page.toString()]);
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

    if (tableParams.customFilters?.search) {
        entries.push(['search', tableParams.customFilters.search]);
    }

    if (tableParams.sorter) {
        const columnsWithOrder: string[] = [];

        for (const [column, ordering] of Object.entries(tableParams.sorter)) {
            columnsWithOrder.push(ordering === 'ascend' ? column : `-${column}`);
        }

        entries.push(['ordering', columnsWithOrder.join(',')]);
    }

    return useMemo(() => new URLSearchParams(entries), [tableParams]);
};
