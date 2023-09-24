import { useMutation } from 'react-query';
import { TransactionPartial, updateTransaction } from '../../api/merger';

export const useUpdateTransaction = () => {
    return useMutation({
        mutationKey: 'update-transaction',
        mutationFn: (transaction: TransactionPartial) =>
            updateTransaction(transaction),
    });
};
