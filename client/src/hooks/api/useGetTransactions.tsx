import { useQuery } from 'react-query';
import { getTransactions } from '../../api/merger';
import { message } from 'antd';
import { Pagination } from '../common';

export const useGetTransactions = (pagination: Pagination) => {
	return useQuery({
		queryKey: ['get-transactions', pagination.page, pagination.pageSize],
		queryFn: () => getTransactions(pagination.page, pagination.pageSize),
		onError: (e) => message.error({ content: e?.toString() }),
	});
};
