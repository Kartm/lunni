import React, { useEffect, useState } from "react";
import { UploadOutlined } from "@ant-design/icons";
import { Button, Form, Modal, Select, Upload } from "antd";
import type { RcFile } from "antd/es/upload/interface";
import { UploadFileVariant } from "../../../api/merger";
import { useForm } from "antd/es/form/Form";
import { useUploadFile } from "../../../hooks/api";

const normFile = (e: any) => {
  if (Array.isArray(e)) {
    return e;
  }
  return e?.fileList;
};

type FileUploadProps = {};

export const FileUploadModal = ({}: FileUploadProps) => {
  const { isLoading, mutate } = useUploadFile();
  const [form] = useForm();

  const onFinish = (values: {
    "variant-select": UploadFileVariant;
    upload: RcFile[];
  }) => {
    mutate({ file: values.upload[0], variant: values["variant-select"] });
  };

  const [open, setOpen] = useState(false);

  useEffect(() => {
    if (!isLoading) {
      form.resetFields();
      setOpen(false);
    }
  }, [isLoading]);

  return (
    <>
      <Button
        type="primary"
        icon={<UploadOutlined />}
        onClick={() => setOpen(true)}
      >
        Upload
      </Button>
      <Modal
        title="Provide bank statement"
        open={open}
        footer={false}
        width={400}
        onCancel={() => {
          form.resetFields();
          setOpen(false);
        }}
      >
        <Form
          form={form}
          labelCol={{ span: 24 }}
          wrapperCol={{ span: 24 }}
          layout="vertical"
          onFinish={onFinish}
          initialValues={{
            "variant-select": "mbank",
          }}
          requiredMark={false}
        >
          <Form.Item name="variant-select" rules={[{ required: true }]}>
            <Select
              options={[
                { label: "mBank", value: "mbank" },
                { label: "mBank savings", value: "mbank-savings" },
                { label: "PKO BP", value: "pko" },
              ]}
            />
          </Form.Item>

          <Form.Item
            name="upload"
            valuePropName="fileList"
            getValueFromEvent={normFile}
            rules={[
              {
                required: true,
                message: "Please provide a file!",
              },
            ]}
          >
            <Upload maxCount={1} beforeUpload={() => false}>
              <Button icon={<UploadOutlined />}>Select .csv file</Button>
            </Upload>
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" loading={isLoading}>
              Submit
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
};
