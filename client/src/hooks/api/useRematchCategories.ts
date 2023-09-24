import { useMutation, useQueryClient } from 'react-query';
import { postRematchCategories } from '../../api/merger';

export const useRematchCategories = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationKey: 'rematch-categories',
        mutationFn: () => postRematchCategories(),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['get-transactions'] });
            queryClient.invalidateQueries({ queryKey: ['categories-stats'] });
        },
    });
};
