import { Button, Input, InputRef, Select, Space } from 'antd';
import React, { useRef, useState } from 'react';
import { PlusOutlined } from '@ant-design/icons';
import { TransactionCategory } from '../../../models/merger';

type SelectAdderProps = {
	onAddOption: (name: string, variant: TransactionCategory['variant']) => void;
};

export const CategoryAdder = ({ onAddOption }: SelectAdderProps) => {
	const [newOption, setNewOption] = useState({
		name: '',
		variant: 'NEG' as TransactionCategory['variant'],
	});
	const inputRef = useRef<InputRef>(null);

	const onNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
		setNewOption((old) => ({ ...old, name: event.target.value }));
	};

	const onVariantChange = (variant: TransactionCategory['variant']) => {
		setNewOption((old) => ({
			...old,
			variant,
		}));
	};

	const addItem = (
		e: React.MouseEvent<HTMLButtonElement | HTMLAnchorElement>
	) => {
		e.preventDefault();
		onAddOption(newOption.name, newOption.variant);
		setNewOption({ name: '', variant: 'NEG' });

		setTimeout(() => {
			inputRef.current?.focus();
		}, 0);
	};

	return (
		<>
			<Space style={{ padding: '0 8px 4px' }}>
				<Input
					placeholder='Category name'
					ref={inputRef}
					value={newOption.name}
					onChange={onNameChange}
				/>

				<Select
					placeholder='Variant'
					options={['NEG', 'POS', 'IGN'].map((o) => ({
						label: o,
						value: o,
					}))}
					onChange={onVariantChange}
					onMouseDown={(e) => e.stopPropagation()} // prevent parent Select from closing
				/>
			</Space>
			<Button type='text' icon={<PlusOutlined />} onClick={addItem}>
				Add item
			</Button>
		</>
	);
};
