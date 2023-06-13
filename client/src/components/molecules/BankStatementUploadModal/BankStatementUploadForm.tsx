import React, { useMemo } from "react";
import { UploadOutlined } from "@ant-design/icons";
import { Button, Form, FormInstance, Select, Upload } from "antd";
import type { RcFile } from "antd/es/upload/interface";
import { useUploadParsers } from "../../../hooks/api/useUploadParsers";
import { DefaultOptionType } from "antd/es/select";

const normFile = (e: any) => {
  if (Array.isArray(e)) {
    return e;
  }
  return e?.fileList;
};

type BankStatementUploadFormProps = {
  isLoading: boolean;
  form: FormInstance<any>;
  onFinish: (values: { parser: string; file: RcFile }) => void;
};

export const BankStatementUploadForm = ({
  isLoading,
  form,
  onFinish,
}: BankStatementUploadFormProps) => {
  const { data: parsers, isLoading: isSelectLoading } = useUploadParsers();

  const selectOptions: DefaultOptionType[] = useMemo(
    () => parsers?.map((v) => ({ label: v.label, value: v.symbol })) ?? [],
    [parsers]
  );

  return (
    <Form
      form={form}
      labelCol={{ span: 24 }}
      wrapperCol={{ span: 24 }}
      layout="vertical"
      onFinish={(values) =>
        onFinish({ file: values.upload[0], parser: values["parser-select"] })
      }
      requiredMark={false}
    >
      <Form.Item name="parser-select" rules={[{ required: true }]}>
        <Select loading={isSelectLoading} options={selectOptions} />
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
