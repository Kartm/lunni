import {useMutation} from "react-query";
import {uploadFile} from "../../api/merger";
import {RcFile} from "antd/lib/upload";

export const useUploadFile = () => {
    return useMutation({
        mutationKey: 'upload-file',
        mutationFn: (newFile: RcFile) => uploadFile(newFile),
    })
}