import React, { memo } from 'react';
import { Transaction } from '../../../models/merger';

type EntryTableDescriptionCellProps = {
	description: Transaction['description'];
};

function EntryTableDescriptionCell({
	description,
}: EntryTableDescriptionCellProps) {
	return <span title={description}>{description}</span>;
}

export default memo(EntryTableDescriptionCell);
