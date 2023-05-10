import { axios } from "../../config";
import { RcFile } from "antd/lib/upload";
import {
  CategoriesResponse,
  CategoryCreateRequest,
  CategoryMatcherCreateRequest,
  CategoryStatsResponse,
  TransactionMergeRequest,
  TransactionPartial,
  TransactionResponse,
  TransactionUpdateRequest,
  TransactionUpdateResponse,
  UploadFileResponse,
  UploadFileVariant,
} from "./merger.dto";
import { AxiosResponse } from "axios";
import { Transaction } from "../../models/merger";

export const uploadFile = async (file: RcFile, variant: UploadFileVariant) => {
  const formData = new FormData();
  console.log(file);
  // @ts-ignore
  formData.append("file", await file.originFileObj);
  formData.append("variant", variant);

  console.log(formData);
  return axios
    .post<UploadFileResponse>("/merger/upload/", formData, {
      headers: {
        "Content-Type": "multipart/form-data; boundary=WebAppBoundary",
      },
    })
    .then((response) => response.data);
};

export const getTransactions = (page: number, pageSize: number) =>
  axios
    .get<TransactionResponse>(
      `/merger/transactions/?page=${page}&page_size=${pageSize}`
    )
    .then((response) => response.data);

export const postMergeTransactions = (merge: TransactionMergeRequest) =>
  axios
    .post<TransactionResponse>("/merger/merge/", merge)
    .then((response) => response.data);

export const postRematchCategories = () =>
  axios.post("/merger/categories/rematch/").then((response) => response.data);

export const getCategoryStats = () =>
  axios
    .get<CategoryStatsResponse>("/merger/categories/stats/")
    .then((response) => response.data);

export const getCategories = () =>
  axios
    .get<CategoriesResponse>(`/merger/categories/`)
    .then((response) => response.data);

export const createCategory = (data: CategoryCreateRequest) =>
  axios
    .post<CategoryCreateRequest>(`/merger/categories/`, data)
    .then((response) => response.data);

export const createCategoryMatcher = (data: CategoryMatcherCreateRequest) =>
  axios
    .post<CategoryMatcherCreateRequest>(`/merger/categories/matchers/`, data)
    .then((response) => response.data);

export const getRegexMatches = (regexExpression: string) =>
  axios
    .get<TransactionResponse>(
      `/merger/transactions/regex-match/?regex_expression=${regexExpression}`
    )
    .then((response) => response.data);

export const updateTransaction = ({
  id,
  ...partialTransaction
}: TransactionPartial) =>
  axios
    .patch<TransactionUpdateRequest, AxiosResponse<TransactionUpdateResponse>>(
      `/merger/transactions/${id}/`,
      partialTransaction
    )
    .then((response) => response.data);
