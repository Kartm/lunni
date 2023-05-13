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

export const uploadFile = async (file: RcFile, variant: UploadFileVariant) => {
  const formData = new FormData();
  // @ts-ignore probably types are outdated, I know it's there...
  formData.append("file", await file.originFileObj);
  formData.append("variant", variant);

  return axios
    .post<UploadFileResponse>("/transactions/upload/", formData, {
      headers: {
        "Content-Type": "multipart/form-data; boundary=WebAppBoundary",
      },
    })
    .then((response) => response.data);
};

export const getTransactions = (page: number, pageSize: number) =>
  axios
    .get<TransactionResponse>(
      `/transactions/?page=${page}&page_size=${pageSize}`
    )
    .then((response) => response.data);

export const postMergeTransactions = (merge: TransactionMergeRequest) =>
  axios
    .post<TransactionResponse>("/transactions/merge/", merge)
    .then((response) => response.data);

export const postRematchCategories = () =>
  axios.post("/categories/rematch/").then((response) => response.data);

export const getCategoryStats = () =>
  axios
    .get<CategoryStatsResponse>("/categories/stats/")
    .then((response) => response.data);

export const getCategories = () =>
  axios
    .get<CategoriesResponse>(`/categories/`)
    .then((response) => response.data);

export const createCategory = (data: CategoryCreateRequest) =>
  axios
    .post<CategoryCreateRequest>(`/categories/`, data)
    .then((response) => response.data);

export const createCategoryMatcher = (data: CategoryMatcherCreateRequest) =>
  axios
    .post<CategoryMatcherCreateRequest>(`/categories/matchers/`, data)
    .then((response) => response.data);

export const getRegexMatches = (regexExpression: string) =>
  axios
    .get<TransactionResponse>(
      `/transactions/regex-match/?regex_expression=${regexExpression}`
    )
    .then((response) => response.data);

export const updateTransaction = ({
  id,
  ...partialTransaction
}: TransactionPartial) =>
  axios
    .patch<TransactionUpdateRequest, AxiosResponse<TransactionUpdateResponse>>(
      `/transactions/${id}/`,
      partialTransaction
    )
    .then((response) => response.data);
