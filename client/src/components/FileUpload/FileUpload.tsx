import React, { useState } from 'react';
import { UploadOutlined } from '@ant-design/icons';
import {Button, message, Space, Upload} from 'antd';
import type { RcFile, UploadFile, UploadProps } from 'antd/es/upload/interface';

type FileUploadProps = {
    isUploading: boolean;
    onFileUpload: (file: RcFile) => void;
}

export const FileUpload = ({isUploading, onFileUpload}:FileUploadProps) => {
    const [fileList, setFileList] = useState<UploadFile[]>([]);

    const handleUpload = () => {
        onFileUpload(fileList[0] as RcFile);
    };

    const props: UploadProps = {
        onRemove: (file) => {
            const index = fileList.indexOf(file);
            const newFileList = fileList.slice();
            newFileList.splice(index, 1);
            setFileList(newFileList);
        },
        beforeUpload: (file) => {
            setFileList([...fileList, file]);

            return false;
        },
        fileList,
    };

    return (
        <Space.Compact>
            <Upload {...props} maxCount={1}>
                <Button icon={<UploadOutlined />}>Select File</Button>
            </Upload>
            <Button
                type="primary"
                onClick={handleUpload}
                disabled={fileList.length === 0}
                loading={isUploading}
            >
                {isUploading ? 'Uploading' : 'Upload'}
            </Button>
        </Space.Compact>
    );
};