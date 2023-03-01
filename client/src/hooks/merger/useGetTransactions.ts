import {useQuery} from "react-query";
import {getTransactions} from "../../api/merger";

export const useGetTransactions = () => {
    return useQuery({
        queryKey: 'get-transactions',
        queryFn: () => getTransactions(),
    })
}