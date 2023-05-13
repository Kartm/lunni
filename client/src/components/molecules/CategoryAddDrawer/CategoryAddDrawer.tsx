import { Button, Drawer, Form, List, Space } from "antd";
import React, { useEffect } from "react";
import { DataType } from "../../organisms/EntryTable";
import TextArea from "antd/es/input/TextArea";
import { SelectWithAdder } from "../SelectWithAdder";
import { useCreateCategory } from "../../../hooks/api/useCreateCategory";
import { useCategoryList } from "../../../hooks/api/useCategoryList";
import { useCreateCategoryMatcher } from "../../../hooks/api/useCreateCategoryMatcher";
import { CategoryMatcherCreateRequest } from "../../../api/merger";
import { useGetRegexMatches } from "../../../hooks/api/useGetRegexMatches";
import { useDebouncedFormValue } from "../../../hooks/common/useDebouncedFormValue";

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

  const regex = useDebouncedFormValue<string>(["regexExpression"], form);
  const { data: regexMatchesList } = useGetRegexMatches(regex);

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
