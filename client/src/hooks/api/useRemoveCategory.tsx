import { useMutation, useQueryClient } from 'react-query';
import {
	removeCategory,
} from '../../api/merger';

export const useRemoveCategory = () => {
	const queryClient = useQueryClient();

	return useMutation({
		mutationKey: 'remove-category',
		mutationFn: (id: number) => removeCategory(id),
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ['get-categories'] });
		},
	});
};
