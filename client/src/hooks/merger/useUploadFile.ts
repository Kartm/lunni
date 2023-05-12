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
    onSuccess: ({ new_entries }) => {
      message.info({
        content: `Uploaded ${new_entries} new records.`,
        duration: 5,
      });

      if (new_entries > 0) {
        queryClient.invalidateQueries({ queryKey: ["get-transactions"] });
        queryClient.invalidateQueries({ queryKey: ["categories-stats"] });
      }
    },
  });
};
