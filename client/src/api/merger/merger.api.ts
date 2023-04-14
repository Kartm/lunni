import { axios } from "../../config";
import { RcFile } from "antd/lib/upload";
import {
  TransactionMergeRequest,
  TransactionResponse,
  UploadFileResponse,
} from "./merger.dto";

export const uploadFile = (file: RcFile) => {
  const formData = new FormData();
  formData.append("file", file);

  return axios
    .post<UploadFileResponse>("/merger/upload/", formData, {
      headers: {
        "Content-Type": "multipart/form-data; boundary=WebAppBoundary",
      },
    })
    .then((response) => response.data);
};

export const getTransactions = () =>
  axios
    .get<TransactionResponse>("/merger/transactions/")
    .then((response) => response.data);

export const postMergeTransactions = (merge: TransactionMergeRequest) =>
  axios
    .post<TransactionResponse>("/merger/merge/", merge)
    .then((response) => response.data);

export const postRematchCategories = () =>
  axios.post("/merger/categories/rematch/").then((response) => response.data);
