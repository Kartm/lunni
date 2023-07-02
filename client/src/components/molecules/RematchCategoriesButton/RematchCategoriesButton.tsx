import { Button, Typography } from 'antd';
import React, { useMemo } from 'react';
import { useRematchCategories } from '../../../hooks/api/useRematchCategories';
import { useCategoryStats } from '../../../hooks/api/useCategoryStats';
import { RedoOutlined } from '@ant-design/icons';

const { Text } = Typography;

export const RematchCategoriesButton = () => {
	const { mutate, isLoading: isRematchLoading } = useRematchCategories();
	const { data } = useCategoryStats();

	const missingCategories =
		useMemo(
			() => data?.find((d) => d.categoryName === null)?.totalCount,
			[data]
		) || 0;

	return (
		<Button
			type='dashed'
			loading={isRematchLoading}
			onClick={() => mutate()}
			icon={<RedoOutlined />}
		>
			<Text>Re-categorize</Text>&nbsp;
			<Text
				strong
				title={
					missingCategories
						? `${missingCategories} records have a missing category`
						: undefined
				}
			>
				{missingCategories}
			</Text>
		</Button>
	);
};
