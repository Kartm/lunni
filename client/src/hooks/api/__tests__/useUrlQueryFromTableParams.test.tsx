import { renderHook } from '@testing-library/react';
import { TableParams } from '../../../components/organisms/EntryTable';
import { useUrlQueryFromTableParams } from '../useUrlQueryFromTableParams';

describe('useUrlQueryFromTableParams', () => {
    test('converts table params to URL query', async () => {
        const props: TableParams = {
            pagination: {
                current: 1,
                pageSize: 50,
            },
            filters: {
                category: ['Income', 'None'],
            },
        };

        const { result } = renderHook<unknown, TableParams>(() => useUrlQueryFromTableParams(props));

        expect(result.current?.toString()).toBe('page=1&page_size=50&category=Income&category=None');
    });
});

