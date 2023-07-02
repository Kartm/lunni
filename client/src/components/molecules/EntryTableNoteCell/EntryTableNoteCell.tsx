import { Input } from 'antd';
import React, { memo } from 'react';
import { Transaction } from '../../../models/merger';

type EntryTableNoteCellProps = {
	defaultNote: Transaction['note'];
	onNoteChange: (note: Transaction['note']) => void;
};

function EntryTableNoteCell({
	defaultNote,
	onNoteChange,
}: EntryTableNoteCellProps) {
	return (
		<Input
			defaultValue={defaultNote}
			onChange={(e) => onNoteChange(e.target.value)}
			allowClear
		/>
	);
}

export default memo(EntryTableNoteCell);
