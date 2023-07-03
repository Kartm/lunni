import { useQuery } from 'react-query';
import { getCategoryMatchers } from '../../api/merger';
import { message } from 'antd';

export const useGetCategoryMatchers = () => {
	return useQuery({
		queryKey: ['get-transactions'],
		queryFn: () => getCategoryMatchers(),
		onError: (e) => message.error({ content: e?.toString() }),
	});
};
