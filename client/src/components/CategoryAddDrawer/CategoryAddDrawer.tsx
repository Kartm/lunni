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
import React, { useCallback, useEffect, useState } from "react";
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
import useDebounce from "antd/es/form/hooks/useDebounce";
import { debounce } from "lodash"; // todo replace this
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
  const [form] = Form.useForm();

  const { data, isLoading: isListLoading } = useCategoryList();
  const { mutate } = useCreateCategory();

  const { mutate: createMatcher } = useCreateCategoryMatcher();

  const regexExpression = Form.useWatch(["regexExpression"], form) as string;
  const [debouncedRegex, setDebouncedRegex] = useState(regexExpression);

  const handleRegexChange = useCallback(
    debounce((regex: string) => setDebouncedRegex(regex), 250),
    [setDebouncedRegex]
  );

  useEffect(() => {
    handleRegexChange(regexExpression);
  }, [regexExpression]);

  const { data: regexMatchesList } = useGetRegexMatches(debouncedRegex);

  useEffect(() => {
    if (!record) {
      return;
    }

    form.setFieldsValue({
      regexExpression: `${record.date} ${record.description}`,
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
      title="New category matcher"
      placement="right"
      onClose={onClose}
      open={!!record}
      width={450}
      bodyStyle={{ paddingBottom: 80 }}
      extra={
        <Space>
          <Button onClick={onClose}>Cancel</Button>
          <Button onClick={onSubmit} type="primary">
            Add
          </Button>
        </Space>
      }
    >
      <Form layout="vertical" requiredMark={false} form={form}>
        <Form.Item
          name="regexExpression"
          label="REGEX to select records"
          rules={[{ required: true, message: "Please enter regex expression" }]}
        >
          <TextArea placeholder="Please enter regex expression" autoSize />
        </Form.Item>
        <Form.Item
          name="category"
          label="Category to assign"
          rules={[{ required: true, message: "Please select a category" }]}
        >
          <SelectWithAdder
            placeholder="Category"
            loading={isListLoading}
            options={data?.results?.map((d) => ({
              label: `${d.name} (${d.variant})`,
              value: d.id,
            }))}
            onAddOption={(name, variant) => mutate({ name, variant })}
          />
        </Form.Item>
        Currently matches {regexMatchesList?.count} records:
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
      </Form>
    </Drawer>
  );
};
