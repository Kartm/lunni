import {useMutation, useQueryClient} from "react-query";
import {postMergeTransactions, TransactionMergeRequest, uploadFile} from "../../api/merger";
import {RcFile} from "antd/lib/upload";

export const useMergeMutations = () => {
    const queryClient = useQueryClient()

    return useMutation({
        mutationKey: 'merge-mutations',
        mutationFn: (merge: TransactionMergeRequest) => postMergeTransactions(merge),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['get-transactions'] })
        }
    })
}