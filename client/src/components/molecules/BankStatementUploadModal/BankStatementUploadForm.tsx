import React from "react";
import { UploadOutlined } from "@ant-design/icons";
import { Button, Form, FormInstance, Select, Upload } from "antd";
import type { RcFile } from "antd/es/upload/interface";
import { UploadFileVariant } from "../../../api/merger";

const normFile = (e: any) => {
  if (Array.isArray(e)) {
    return e;
  }
  return e?.fileList;
};

type BankStatementUploadFormProps = {
  isLoading: boolean;
  form: FormInstance<any>;
  onFinish: (values: { variant: UploadFileVariant; file: RcFile }) => void;
};

export const BankStatementUploadForm = ({
  isLoading,
  form,
  onFinish,
}: BankStatementUploadFormProps) => {
  return (
    <Form
      form={form}
      labelCol={{ span: 24 }}
      wrapperCol={{ span: 24 }}
      layout="vertical"
      onFinish={(values) =>
        onFinish({ file: values.upload[0], variant: values["variant-select"] })
      }
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
  );
};
