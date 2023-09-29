import React, { useEffect, useState } from 'react';
import { Input, Table, TablePaginationConfig, DatePicker, Pagination } from 'antd';
import { Transaction } from '../../../models/merger';
import { FilterValue, Key, SorterResult } from 'antd/es/table/interface';
import { TransactionPartial } from '../../../api/merger';
import { debounce } from 'lodash';
import { useEntryTableColumns, useEntryTableRows } from '../../../hooks/components';
import { RangeValue } from 'rc-picker/lib/interface';
import dayjs from 'dayjs';

const { RangePicker } = DatePicker;

export type DataType = Transaction & {
    key: Key;
};

type DateFilters = 'date_after' | 'date_before';

export type TableParams = {
    pagination?: TablePaginationConfig;
    filters?: Record<string | DateFilters, FilterValue | null>;
    sorter?: SorterResult<DataType>;
    searchRegex?: string;
}

type EntryTableProps = {
    totalEntries?: number;
    isLoading?: boolean;
    data: Transaction[];
    selection: Key[];
    onSelectionChange: (keys: Key[]) => void;
    onChange: (params: TableParams) => void;
    onCategoryAdd: (record: DataType) => void;
    onRecordUpdate: (transactionPartial: TransactionPartial) => void;
    mergeComponent: ({ record }: { record: DataType }) => React.ReactNode;
};

export const EntryTable = ({
    isLoading,
    data,
    totalEntries,
    selection,
    onSelectionChange,
    onChange,
    onCategoryAdd,
    onRecordUpdate,
    mergeComponent,
}: EntryTableProps) => {
    const { dataSource, disabledRows, onRowSelectionChange } = useEntryTableRows({
        data,
        selection,
        onSelectionChange,
    });
    const [tableParams, setTableParams] = useState<TableParams>({
        pagination: {
            current: 1,
            pageSize: 50,
            total: totalEntries,
            showSizeChanger: true,
            pageSizeOptions: [50, 100, 500, 1000],
            position: ['topRight'],
        },
    });

    const onRecordUpdateDebounced = debounce(onRecordUpdate, 250);
    const columns = useEntryTableColumns({
        onCategoryAdd,
        onRecordUpdate: onRecordUpdateDebounced,
    });

    useEffect(() => {
        onChange(tableParams);
    }, [JSON.stringify(tableParams)]); // todo performance and anti-pattern

    useEffect(() => setTableParams(prev => ({
        ...prev,
        pagination: { ...prev.pagination, total: totalEntries },
    })), [totalEntries]); // todo performance and anti-pattern

    const handleTableChange = (
        pagination: TablePaginationConfig,
        filters: Record<string, FilterValue | null>,
        sorter: SorterResult<DataType> | SorterResult<DataType>[],
    ) => {
        setTableParams(prev => ({
            pagination: { ...prev.pagination },
            filters: { ...prev.filters, ...filters },
            sorter: { ...prev.sorter, ...sorter },
        }));
    };

    const onSearchChange = (searchRegex?: string) => {
        setTableParams(p => ({ ...p, searchRegex }))
    }

    const onSearchChangeDebounced = debounce(onSearchChange, 250);
 // todo pagination extract and put separately. use HOC to reduce rerenders

    const onDateFilterChange = (range: RangeValue<dayjs.Dayjs>) => {
        console.log(range);

        if (range == null) {
            setTableParams(prev => {
                if (!prev.filters) {
                    return prev;
                }

                const {date_after, date_before, ...filtersWithoutDate} = prev.filters;

                return {
                    pagination: { ...prev.pagination },
                    filters: { ...filtersWithoutDate },
                    sorter: { ...prev.sorter },
                }
            });
        } else if (range[0] && range[1]) {
            setTableParams(prev => ({
                pagination: { ...prev.pagination },
                filters: { ...prev.filters, 'date_after': [range[0]!.format('YYYY-MM-DD')], 'date_before': [range[1]!.format('YYYY-MM-DD')] },
                sorter: { ...prev.sorter },
            }));
        }
    };

    const onPaginationChange = (page: number, pageSize: number) => {
        setTableParams(prev => {
            const hasPageSizeChanged = pageSize !== prev.pagination?.pageSize;

            return {
                ...prev,
                pagination: { ...prev.pagination, current: hasPageSizeChanged ? 1 : page, pageSize: pageSize },
            }
        });
    }

    return (
        <>
            <Table
            title={() => <>
                <Input placeholder={'Visit to (museum|restaurant)'} allowClear
                       onChange={(e) => onSearchChangeDebounced(e.target.value)}></Input>
                <RangePicker onChange={(range) => onDateFilterChange(range)} />
                <Pagination
                    showSizeChanger
                    onChange={onPaginationChange}
                    total={totalEntries}
                    current={tableParams.pagination?.current}
                    pageSize={tableParams.pagination?.pageSize}
                />
            </>}
            loading={isLoading}
            dataSource={dataSource}
            columns={columns}
            rowSelection={{
                type: 'checkbox',
                hideSelectAll: true,
                onChange: (selectedRowKeys) => onRowSelectionChange(selectedRowKeys),
                selectedRowKeys: selection,
                getCheckboxProps: (record) => ({
                    disabled: disabledRows.has(record),
                }),
            }}
            onChange={handleTableChange}
            expandable={{
                showExpandColumn: false,
                expandedRowRender: (record) => <div>{mergeComponent({ record })}</div>,
                expandedRowKeys: selection.length === 2 ? [selection[0]] : [],
            }} /></>
    );
};
