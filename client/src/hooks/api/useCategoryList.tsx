import { useQuery } from 'react-query';
import { getCategories } from '../../api/merger';

export const useCategoryList = () => {
    return useQuery({
        queryKey: ['get-categories'],
        queryFn: () => getCategories(),
    });
};
