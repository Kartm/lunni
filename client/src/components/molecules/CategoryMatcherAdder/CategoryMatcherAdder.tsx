import { Button, Drawer, Form, List, Modal, Space, Tooltip } from "antd";
import React, { useEffect, useState } from "react";
import { DataType } from "../../organisms/EntryTable";
import TextArea from "antd/es/input/TextArea";
import { CategorySelect } from "../CategorySelect";
import { useCreateCategory, useRematchCategories } from "../../../hooks/api";
import { useCategoryList } from "../../../hooks/api";
import { useCreateCategoryMatcher } from "../../../hooks/api";
import { CategoryMatcherCreateRequest } from "../../../api/merger";
import { useGetRegexMatches } from "../../../hooks/api";
import { useDebouncedFormValue } from "../../../hooks/common";
import { DeleteOutlined } from "@ant-design/icons";
import { useRemoveCategory } from "../../../hooks/api/useRemoveCategory";
import { useGetCategoryMatchers } from "../../../hooks/api/useGetCategoryMatchers";
import { Typography } from 'antd';

const { Text } = Typography;

type CategoryAddDrawerProps = {
  record?: DataType;
  onClose: () => void;
};

export const CategoryMatcherAdder = ({
  record,
  onClose,
}: CategoryAddDrawerProps) => {
  const [form] = Form.useForm();
  const [removeModalOpen, setRemoveModalOpen] = useState(false);
  const [foundMatchersToRemove, setFoundMatchersToRemove] = useState<string[]>([]);
  const [categoryToRemove, setCategoryToRemove] = useState<number>();

  const { data, isLoading: isListLoading } = useCategoryList();
  const { mutate } = useCreateCategory();
  const { mutate: removeCategory } = useRemoveCategory();

  const { mutate: createMatcher } = useCreateCategoryMatcher();

  const regex = useDebouncedFormValue<string>(["regexExpression"], form);
  const { data: regexMatchesList } = useGetRegexMatches(regex);
  const { data: categoryMatchers, isLoading: categoryMatchersLoading } = useGetCategoryMatchers();
  const { mutate: rematchCategories } = useRematchCategories();

  useEffect(() => {
    if (!record) {
      return;
    }

    form.setFieldsValue({
      regexExpression: `${record.description}`,
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

  const getMatchersWithProvidedCategory = (id: number) => {
    const matchersWithCategories = categoryMatchers?.results.filter(matcher => matcher.category)

    return matchersWithCategories?.filter(matcher => matcher.category.id === id)
  }

  const handleDelete = (id: number, e: any) => {
    e.stopPropagation()

    const matchersWithCategory = getMatchersWithProvidedCategory(id)

    setCategoryToRemove(id)
    if (matchersWithCategory?.length) {
      setFoundMatchersToRemove(matchersWithCategory.map(matcher => matcher.regex_expression))
      setRemoveModalOpen(true)
    } else {
      handleRemoveCategory()
    }
  }

  const handleRemoveCategory = () => {
    if (categoryToRemove) {
      removeCategory({ id: categoryToRemove })
      setCategoryToRemove(undefined)
    }
  }

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
          tooltip={`To match only this specific record you need to provide date in the beggining: ${record?.date} ${record?.description}`}
          rules={[{ required: true, message: "Please enter regex expression" }]}
        >
          <TextArea placeholder="Please enter regex expression" autoSize />
        </Form.Item>
        <Form.Item
          name="category"
          label="Category to assign"
          rules={[{ required: true, message: "Please select a category" }]}
        >
          <CategorySelect
            placeholder="Category"
            loading={isListLoading || categoryMatchersLoading}
            options={data?.results?.map((d) => ({
              label: <>
                {d.name} {d.variant}
                {
                  <Tooltip title="Delete category">
                    <Button type="text" icon={<DeleteOutlined />} onClick={(e) => handleDelete(d.id, e)}></Button>
                  </Tooltip>
                }
              </>,
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
      <Modal title="Remove matchers" open={removeModalOpen} okText={"Remove category"} onOk={() => {
        handleRemoveCategory()
        rematchCategories()
        setRemoveModalOpen(false)
      }}
        onCancel={() => setRemoveModalOpen(open => !open)}>
        <p>This category is used in the following category matchers that will also be removed:</p>
        <Space direction="vertical">
          {foundMatchersToRemove.map(matcher => <Text type="secondary" key={matcher}>{matcher}</Text>)}
        </Space>
      </Modal>
    </Drawer>
  );
};
