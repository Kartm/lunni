import { DataType, Filters } from '../../components/organisms/EntryTable';
import React, { useEffect, useMemo, useState } from 'react';
import { TransactionPartial } from '../../api/merger';
import { ColumnsType, ColumnType } from 'antd/lib/table';
import { EntryTableDescriptionCell } from '../../components/molecules/EntryTableDescriptionCell';
import { EntryTableCategoryCell } from '../../components/molecules/EntryTableCategoryCell';
import { EntryTableNoteCell } from '../../components/molecules/EntryTableNoteCell';
import { EntryTableAmountCell } from '../../components/molecules/EntryTableAmountCell';
import { useCategoryStats } from '../api';
import { DatePicker, Input } from 'antd';
import { debounce } from 'lodash';
import { RangeValue } from 'rc-picker/lib/interface';
import { Dayjs } from 'dayjs';
import { SearchOutlined } from '@ant-design/icons';

const { RangePicker } = DatePicker;

type useEntryTableColumnsProps = {
    onCategoryAdd: (record: DataType) => void;
    onRecordUpdate: (transactionPartial: TransactionPartial) => void;
    onFiltersChange: (filters: Filters) => void;
};

const DATE_FORMAT = 'YYYY-MM-DD';

export const useEntryTableColumns = ({
    onCategoryAdd,
    onRecordUpdate,
    onFiltersChange
}: useEntryTableColumnsProps): ColumnsType<DataType> => {
    const { data: categoryStats } = useCategoryStats();

    const [filters, setFilters] = useState<Filters>({});

    useEffect(() => {
        onFiltersChange(filters);
    }, [filters]);

    const categoryFilters = useMemo(
        () => categoryStats?.map(
            category => ({
                text: `${category.categoryName || '(None)'} (${category.totalCount})`,
                value: category.categoryName || 'None',
            }),
        ) || [],
        [categoryStats]);

    const onSearchChange = (searchRegex?: string) => {
        setFilters(prev => ({ ...prev, search: searchRegex}));
    };

    const onDateFiltersChange = (range: RangeValue<Dayjs>) => {
        if (range === null) {
            setFilters(({ date, ...prevWithoutDate }) => (prevWithoutDate));
        } else if (range[0] && range[1]) {
            const [after, before] = range;
            setFilters(prev => ({ ...prev,
                date: { after: after.format(DATE_FORMAT), before: before.format(DATE_FORMAT) }
            }));
        }
    };

    const onSearchChangeDebounced = debounce(onSearchChange, 250);

    const dateFilterDropdown: ColumnType<DataType>['filterDropdown'] = () =>
        <div style={{ padding: 8 }} onKeyDown={(e) => e.stopPropagation()}>
            <RangePicker
                placeholder={['From date', 'To date']}
                onChange={onDateFiltersChange}
            />
        </div>;

    const descriptionFilterDropdown: ColumnType<DataType>['filterDropdown'] = () =>
        <div style={{ padding: 8 }} onKeyDown={(e) => e.stopPropagation()}>
            <Input
                placeholder={'Visit to (museum|restaurant)'}
                allowClear
                onChange={(e) => onSearchChangeDebounced(e.target.value)}
            />
        </div>;

    return useMemo(
        (): ColumnsType<DataType> => [
            {
                title: 'Date',
                dataIndex: 'date',
                key: 'date',
                width: 115,
                sorter: true,
                filterDropdown: dateFilterDropdown,
                filtered: !!filters.date
            },
            {
                title: 'Description',
                dataIndex: 'description',
                key: 'description',
                ellipsis: true,
                render: (description: string) => (
                    <EntryTableDescriptionCell description={description} />
                ),
                filterDropdown: descriptionFilterDropdown,
                filtered: !!filters.search?.length,
                filterIcon: filtered => <SearchOutlined style={{ fontSize: '16px', color: filtered ? '#1890ff' : undefined }} />
            },
            {
                title: 'Category',
                dataIndex: 'category',
                key: 'category',
                width: 140,
                ellipsis: true,
                render: (category: DataType['category'], record) => (
                    <EntryTableCategoryCell
                        category={category}
                        onClickAdd={() => onCategoryAdd(record)}
                    />
                ),
                filters: categoryFilters,
                filtered: !!filters.categories?.length
            },
            {
                title: 'Note',
                dataIndex: 'note',
                key: 'note',
                width: 150,
                render: (_, record) => (
                    <EntryTableNoteCell
                        defaultNote={record.note}
                        onNoteChange={(note) => onRecordUpdate({ id: record.id, note })}
                    />
                ),
            },
            {
                title: 'Account',
                dataIndex: 'account',
                key: 'account',
                width: 80,
                ellipsis: true,
            },
            {
                title: 'Amount',
                dataIndex: 'calculated_amount',
                key: 'amount',
                width: 150,
                align: 'right',
                render: (amount: number) => <EntryTableAmountCell amount={amount} />,
                sorter: true,
            },
        ],
        [onCategoryAdd, onRecordUpdate],
    );
};
