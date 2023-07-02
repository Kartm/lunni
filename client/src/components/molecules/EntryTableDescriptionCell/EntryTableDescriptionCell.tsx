import React, { memo } from 'react';
import { Transaction } from '../../../models/merger';

type EntryTableDescriptionCellProps = {
	description: Transaction['description'];
};

export const EntryTableDescriptionCell = memo(
	({ description }: EntryTableDescriptionCellProps) => (
		<span title={description}>{description}</span>
	)
);
