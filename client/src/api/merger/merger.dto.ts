import {Transaction} from "../../models/merger";

export type UploadFileResponse = {

}

export type TransactionResponse = {
    transactions: Array<Transaction>
}

export type TransactionMergeRequest = {
    "from_transaction": number,
    "to_transaction": number,
    "amount": number
}