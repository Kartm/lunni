import { renderHook } from '@testing-library/react';
import { TableParams } from '../../../components/organisms/EntryTable';
import { useUrlQueryFromTableParams } from '../useUrlQueryFromTableParams';

describe('useUrlQueryFromTableParams', () => {
    test('converts table pagination to URL query', async () => {
        const props: TableParams = {
            pagination: {
                page: 1,
                pageSize: 50,
            },
        };

        const { result } = renderHook<unknown, TableParams>(() => useUrlQueryFromTableParams(props));

        expect(result.current?.toString()).toBe('page=1&page_size=50');
    });

    test('converts table categories filters to URL query', async () => {
        const props: TableParams = {
            customFilters: {
                categories: ['Income', 'None'],
            },
        };

        const { result } = renderHook<unknown, TableParams>(() => useUrlQueryFromTableParams(props));

        expect(result.current?.toString()).toBe('category=Income&category=None');
    });

    test('converts table date range filters to URL query', async () => {
        const props: TableParams = {
            customFilters: {
                date: {
                    after: '2023-01-10',
                    before: '2023-01-20',
                },
            },
        };

        const { result } = renderHook<unknown, TableParams>(() => useUrlQueryFromTableParams(props));

        expect(result.current?.toString()).toBe('date_after=2023-01-10&date_before=2023-01-20');
    });

    test('converts table sorter to URL query', async () => {
        const props: TableParams = {
            sorter: {
                date: 'descend',
                calculated_amount: 'ascend'
            }
        };

        const { result } = renderHook<unknown, TableParams>(() => useUrlQueryFromTableParams(props));

        expect(result.current?.toString()).toBe('ordering=-date%2Ccalculated_amount');
    });

    test('converts table search to URL query', async () => {
        const props: TableParams = {
            customFilters: {
                search: '2023-01-05 (CompCo|Polex)'
            }
        };

        const { result } = renderHook<unknown, TableParams>(() => useUrlQueryFromTableParams(props));
        expect(result.current?.toString()).toBe('search=2023-01-05+%28CompCo%7CPolex%29');
    });
});

