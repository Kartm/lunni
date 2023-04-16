import {
  Button,
  Card,
  Col,
  Drawer,
  Form,
  Input,
  List,
  Row,
  Select,
  Space,
  Tag,
  Typography,
} from "antd";
import React, { useEffect } from "react";
import { useRematchCategories } from "../../hooks/merger/useRematchCategories";
import { useCategoryStats } from "../../hooks/merger/useCategoryStats";
import { SyncOutlined } from "@ant-design/icons";
import { DataType } from "../EntryTable";
import TextArea from "antd/es/input/TextArea";
import { SelectWithAdder } from "../SelectWithAdder";
import { useCreateCategory } from "../../hooks/merger/useCreateCategory";
import { useCategoryList } from "../../hooks/merger/useCategoryList";
import { useCreateCategoryMatcher } from "../../hooks/merger/useCreateCategoryMatcher";
import { CategoryMatcherCreateRequest } from "../../api/merger";
import { useGetRegexMatches } from "../../hooks/merger/useGetRegexMatches";

const { Text } = Typography;
const { Option } = Select;

type CategoryAddDrawerProps = {
  record?: DataType;
  onClose: () => void;
};

export const CategoryAddDrawer = ({
  record,
  onClose,
}: CategoryAddDrawerProps) => {
  // todo initial regex is record's description
  const [form] = Form.useForm();

  const { data, isLoading: isListLoading } = useCategoryList();
  const { mutate } = useCreateCategory();

  const { mutate: createMatcher } = useCreateCategoryMatcher();

  const regexExpression = Form.useWatch(["regexExpression"], form);
  const { data: regexMatchesList } = useGetRegexMatches(regexExpression);

  useEffect(() => {
    if (!record) {
      return;
    }

    form.setFieldsValue({
      regexExpression: record.description,
    });
  }, [record]);

  const onSubmit = () => {
    const matcher: CategoryMatcherCreateRequest = {
      regex_expression: form.getFieldValue(["regexExpression"]),
      category_id: form.getFieldValue(["category"]),
    };

    createMatcher(matcher);
    onClose();
  };

  return (
    <Drawer
      title="Add category"
      placement="right"
      onClose={onClose}
      open={!!record}
      bodyStyle={{ paddingBottom: 80 }}
      extra={
        <Space>
          <Button onClick={onClose}>Cancel</Button>
          <Button onClick={onSubmit} type="primary">
            Submit
          </Button>
        </Space>
      }
    >
      <Form layout="vertical" hideRequiredMark form={form}>
        <Row gutter={16}>
          <Col span={24}>
            <Form.Item
              name="regexExpression"
              label="Regex expression"
              rules={[
                { required: true, message: "Please enter regex expression" },
              ]}
            >
              <TextArea placeholder="Please enter regex expression" autoSize />
            </Form.Item>
            {regexMatchesList?.count} matches:
            <List
              bordered
              dataSource={regexMatchesList?.results}
              itemLayout="horizontal"
              renderItem={(item) => (
                <List.Item>
                  <List.Item.Meta
                    title={item.date}
                    description={`${item.description}, ${item.amount}`}
                  />
                </List.Item>
              )}
            />
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={24}>
            <Form.Item
              name="category"
              label="Category to match"
              rules={[{ required: true, message: "Please select a category" }]}
            >
              <SelectWithAdder
                loading={isListLoading}
                options={data?.results?.map((d) => ({
                  label: `${d.name} (${d.variant})`,
                  value: d.id,
                }))}
                onAddOption={(name) => mutate({ name, variant: "NEG" })}
              />
            </Form.Item>
          </Col>
        </Row>
      </Form>
    </Drawer>
  );
};
