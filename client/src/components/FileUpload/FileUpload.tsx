import React, { useState } from "react";
import { UploadOutlined } from "@ant-design/icons";
import { Button, Form, message, Select, Space, Upload } from "antd";
import type { RcFile, UploadFile, UploadProps } from "antd/es/upload/interface";
import { UploadFileVariant } from "../../api/merger";

const { Option } = Select;

const normFile = (e: any) => {
  console.log("Upload event:", e);
  if (Array.isArray(e)) {
    return e;
  }
  return e?.fileList;
};

type FileUploadProps = {
  isUploading: boolean;
  onFileUpload: (file: RcFile, variant: UploadFileVariant) => void;
};

export const FileUpload = ({ isUploading, onFileUpload }: FileUploadProps) => {
  const formItemLayout = { wrapperCol: { span: 24 } };
  const buttonItemLayout = { wrapperCol: { span: 10, offset: 4 } };

  const onFinish = (values: {
    "variant-select": UploadFileVariant;
    upload: RcFile[];
  }) => {
    onFileUpload(values.upload[0], values["variant-select"]);
  };

  return (
    <Form
      name="validate_other"
      {...formItemLayout}
      layout="vertical"
      onFinish={onFinish}
      initialValues={{
        "variant-select": "mbank",
      }}
      style={{ maxWidth: 600 }}
    >
      <Form.Item name="variant-select" rules={[{ required: true }]}>
        <Select placeholder="Source .csv bank">
          <Option value="mbank">mBank</Option>
          <Option value="pko">PKO BP</Option>
        </Select>
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
          <Button icon={<UploadOutlined />}>Select File</Button>
        </Upload>
      </Form.Item>

      <Form.Item {...buttonItemLayout}>
        <Space>
          <Button type="primary" htmlType="submit" loading={isUploading}>
            Submit
          </Button>
          <Button htmlType="reset">reset</Button>
        </Space>
      </Form.Item>
    </Form>
  );
};
