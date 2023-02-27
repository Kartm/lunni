import {axios} from "../../config";
import {RcFile} from "antd/lib/upload";

export const uploadFile = (file: RcFile) => {
    const formData = new FormData();
    formData.append('file', file);

    return axios.post('/files/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data; boundary=WebAppBoundary',
        }
    }).then(response => response.data);
}