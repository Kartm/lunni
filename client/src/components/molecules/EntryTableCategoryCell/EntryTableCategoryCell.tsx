import { Button, Typography } from 'antd';
import React, { memo } from 'react';
import { PlusCircleOutlined } from '@ant-design/icons';
import { Transaction } from '../../../models/merger';

const { Text } = Typography;

type EntryTableCategoryCellProps = {
	category?: Transaction['category'];
	onClickAdd: () => void;
};

function EntryTableCategoryCell({
	category,
	onClickAdd,
}: EntryTableCategoryCellProps) {
	return (
		<Text
			type={
				category?.variant === 'POS'
					? 'success'
					: category?.variant === 'NEG'
						? 'danger'
						: 'secondary'
			}
		>
			{category?.name || (
				<Button
					icon={<PlusCircleOutlined />}
					size={'small'}
					type={'ghost'}
					title={'Category is missing'}
					onClick={() => onClickAdd()}
				/>
			)}
		</Text>
	);
}

export default memo(EntryTableCategoryCell);
