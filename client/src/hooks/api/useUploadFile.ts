import { uploadFile } from "../../api/merger";
import { RcFile } from "antd/lib/upload";
import { message } from "antd";
import { useMutation, useQueryClient } from "react-query";

type useUploadFileProps = {
  onSuccess: () => void;
};

export const useUploadFile = ({ onSuccess }: useUploadFileProps) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationKey: "upload-file",
    mutationFn: ({ file, parser }: { file: RcFile; parser: string }) =>
      uploadFile(file, parser),
    onSuccess: ({ new_entries }) => {
      message.info({
        content: `Uploaded ${new_entries} new records.`,
        duration: 5,
      });

      if (new_entries > 0) {
        queryClient.invalidateQueries({ queryKey: ["get-transactions"] });
        queryClient.invalidateQueries({ queryKey: ["categories-stats"] });
      }

      onSuccess();
    },
  });
};
