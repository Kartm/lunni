import { useQuery } from 'react-query';
import { getUploadParsers } from '../../api/merger';

export const useUploadParsers = () => {
	return useQuery({
		queryKey: ['get-upload-parsers'],
		queryFn: () => getUploadParsers(),
	});
};
