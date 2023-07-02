import { Divider, Select } from 'antd';
import React, { useState } from 'react';
import { SelectProps } from 'antd/es/select';
import { TransactionCategory } from '../../../models/merger';
import { CategoryAdder } from './CategoryAdder';

type SelectWithAdderProps = {
	onAddOption: (name: string, variant: TransactionCategory['variant']) => void;
} & Omit<SelectProps, 'open'>;

export const CategorySelect = ({
	onAddOption,
	...props
}: SelectWithAdderProps) => {
	const [open, setOpen] = useState(false);

	const handleAddOption = (
		name: string,
		variant: TransactionCategory['variant']
	) => {
		onAddOption(name, variant);
		setOpen(false);
	};

	return (
		<Select
			{...props}
			open={open}
			onDropdownVisibleChange={(visible) => setOpen(visible)}
			dropdownRender={(menu) => (
				<>
					{menu}
					<Divider style={{ margin: '8px 0' }} />
					<CategoryAdder onAddOption={handleAddOption} />
				</>
			)}
			{...props}
		/>
	);
};
