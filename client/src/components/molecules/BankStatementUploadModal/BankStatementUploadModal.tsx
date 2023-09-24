import React, { useState } from 'react';
import { UploadOutlined } from '@ant-design/icons';
import { Button, Modal } from 'antd';
import { useForm } from 'antd/es/form/Form';
import { useUploadFile } from '../../../hooks/api';
import { BankStatementUploadForm } from './BankStatementUploadForm';

export const BankStatementUploadModal = () => {
    const [form] = useForm();
    const [open, setOpen] = useState(false);

    const closeModal = () => {
        form.resetFields();
        setOpen(false);
    };

    const { isLoading, mutate } = useUploadFile({ onSuccess: closeModal });

    return (
        <>
            <Button
                type='primary'
                icon={<UploadOutlined />}
                onClick={() => setOpen(true)}
            >
                Upload
            </Button>
            <Modal
                title='Provide bank statement'
                open={open}
                footer={false}
                width={400}
                onCancel={() => closeModal()}
            >
                <BankStatementUploadForm
                    isLoading={isLoading}
                    form={form}
                    onFinish={(values) => mutate(values)}
                />
            </Modal>
        </>
    );
};
