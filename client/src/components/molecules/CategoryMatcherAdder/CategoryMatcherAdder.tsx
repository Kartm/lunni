import { Button, Drawer, Form, List, Space } from 'antd';
import React, { useEffect } from 'react';
import { DataType } from '../../organisms/EntryTable';
import TextArea from 'antd/es/input/TextArea';
import { CategorySelect } from '../CategorySelect';
import { useCreateCategory } from '../../../hooks/api';
import { useCategoryList } from '../../../hooks/api';
import { useCreateCategoryMatcher } from '../../../hooks/api';
import { CategoryMatcherCreateRequest } from '../../../api/merger';
import { useGetRegexMatches } from '../../../hooks/api';
import { useDebouncedFormValue } from '../../../hooks/common';

type CategoryAddDrawerProps = {
	record?: DataType;
	onClose: () => void;
};

export const CategoryMatcherAdder = ({
	record,
	onClose,
}: CategoryAddDrawerProps) => {
	const [form] = Form.useForm();

	const { data, isLoading: isListLoading } = useCategoryList();
	const { mutate } = useCreateCategory();

	const { mutate: createMatcher } = useCreateCategoryMatcher();

	const regex = useDebouncedFormValue<string>(['regexExpression'], form);
	const { data: regexMatchesList } = useGetRegexMatches(regex);

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
			regex_expression: form.getFieldValue(['regexExpression']),
			category_id: form.getFieldValue(['category']),
		};

		createMatcher(matcher);
		onClose();
	};

	return (
		<Drawer
			title='New category matcher'
			placement='right'
			onClose={onClose}
			open={!!record}
			width={450}
			bodyStyle={{ paddingBottom: 80 }}
			extra={
				<Space>
					<Button onClick={onClose}>Cancel</Button>
					<Button onClick={onSubmit} type='primary'>
						Add
					</Button>
				</Space>
			}
		>
			<Form layout='vertical' requiredMark={false} form={form}>
				<Form.Item
					name='regexExpression'
					label='REGEX to select records'
					tooltip={`To match only this specific record you need to provide date in the beggining: ${record?.date} ${record?.description}`}
					rules={[{ required: true, message: 'Please enter regex expression' }]}
				>
					<TextArea placeholder='Please enter regex expression' autoSize />
				</Form.Item>
				<Form.Item
					name='category'
					label='Category to assign'
					rules={[{ required: true, message: 'Please select a category' }]}
				>
					<CategorySelect
						placeholder='Category'
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
					itemLayout='horizontal'
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
