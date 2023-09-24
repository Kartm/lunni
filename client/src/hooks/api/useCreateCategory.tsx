import { useMutation, useQueryClient } from 'react-query';
import { CategoryCreateRequest, createCategory } from '../../api/merger';

export const useCreateCategory = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationKey: 'create-category',
        mutationFn: (category: CategoryCreateRequest) => createCategory(category),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['get-categories'] });
        },
    });
};
