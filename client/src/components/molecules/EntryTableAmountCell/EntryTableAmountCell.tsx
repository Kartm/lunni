import { Typography } from 'antd';
import React, { memo } from 'react';
import { Transaction } from '../../../models/merger';

const { Text } = Typography;

type EntryTableAmountCellProps = {
	amount: Transaction['amount'];
};

export const EntryTableAmountCell = memo(
	({ amount }: EntryTableAmountCellProps) => (
		<Text type={amount > 0 ? 'success' : 'danger'}>
			{`${(amount / 100).toFixed(2)} PLN`}
		</Text>
	)
);
