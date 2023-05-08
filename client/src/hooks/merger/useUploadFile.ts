import { useMutation } from "react-query";
import { uploadFile, UploadFileVariant } from "../../api/merger";
import { RcFile } from "antd/lib/upload";

export const useUploadFile = () => {
  return useMutation({
    mutationKey: "upload-file",
    mutationFn: ({
      file,
      variant,
    }: {
      file: RcFile;
      variant: UploadFileVariant;
    }) => uploadFile(file, variant),
  });
};
