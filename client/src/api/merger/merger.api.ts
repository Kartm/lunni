import {axios} from "../../config";
import {RcFile} from "antd/lib/upload";
import {TransactionResponse} from "./merger.dto";
import {AxiosResponse} from "axios";

export const uploadFile = (file: RcFile) => {
    const formData = new FormData();
    formData.append('file', file);

    return axios.post('/merger/upload/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data; boundary=WebAppBoundary',
        }
    }).then(response => response.data);
}

export const getTransactions = () => axios.get<TransactionResponse>('/merger/transactions/').then(response => response.data)