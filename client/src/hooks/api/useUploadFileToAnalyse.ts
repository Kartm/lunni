import { uploadFileToAnalyse } from "../../api/merger";
import { useMutation } from "react-query";

export const useUploadFileToAnalyse = () => {
  return useMutation({
    mutationKey: "analyse-upload",
    mutationFn: (file) =>
      uploadFileToAnalyse(file),
    onSuccess: (data) => {
        console.log(data)
    },
  });
};
