import { useQuery } from 'react-query';
import { getCategoryStats } from '../../api/merger';

export const useCategoryStats = () => {
    return useQuery({
        queryKey: 'categories-stats',
        queryFn: () => getCategoryStats(),
    });
};
