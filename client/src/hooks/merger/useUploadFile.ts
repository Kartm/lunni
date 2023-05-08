import { uploadFile, UploadFileVariant } from "../../api/merger";
import { RcFile } from "antd/lib/upload";
import { message } from "antd";
import { useMutation, useQueryClient } from "react-query";

export const useUploadFile = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationKey: "upload-file",
    mutationFn: ({
      file,
      variant,
    }: {
      file: RcFile;
      variant: UploadFileVariant;
    }) => uploadFile(file, variant),
    onSuccess: (data) => {
      message.info({ content: `Uploaded ${data.new_entries} new records` });

      if (data.new_entries > 0) {
        queryClient.invalidateQueries({ queryKey: ["rematch-categories"] });
      }
    },
  });
};
