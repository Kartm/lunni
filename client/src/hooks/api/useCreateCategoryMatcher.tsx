import { useMutation, useQueryClient } from 'react-query';
import {
	CategoryMatcherCreateRequest,
	createCategoryMatcher,
} from '../../api/merger';
import { useRematchCategories } from './useRematchCategories';

export const useCreateCategoryMatcher = () => {
	const queryClient = useQueryClient();

	const { mutate: rematchCategories } = useRematchCategories();

	return useMutation({
		mutationKey: 'create-category-matcher',
		mutationFn: (matcher: CategoryMatcherCreateRequest) =>
			createCategoryMatcher(matcher),
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ['get-category-matchers'] });
			rematchCategories();
		},
	});
};
