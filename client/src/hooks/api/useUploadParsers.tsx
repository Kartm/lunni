import { useQuery } from "react-query";
import {
  getCategories,
  getTransactions,
  getUploadParsers,
} from "../../api/merger";
import { message } from "antd";

export const useUploadParsers = () => {
  return useQuery({
    queryKey: ["get-upload-parsers"],
    queryFn: () => getUploadParsers(),
  });
};
