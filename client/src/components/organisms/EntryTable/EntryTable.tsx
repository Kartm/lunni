import React, {useEffect, useState} from 'react';
import {Table, TablePaginationConfig} from 'antd';
import {Transaction} from '../../../models/merger';
import {FilterValue, Key, SorterResult} from 'antd/es/table/interface';
import {TransactionPartial} from '../../../api/merger';
import {debounce} from 'lodash';
import {useEntryTableColumns, useEntryTableRows} from '../../../hooks/components';

export type DataType = Transaction & {
    key: Key;
};

export type Filters = { date?: { before: string, after: string }, search?: string, categories?: (string | null)[] };

export type TableParams = {
    pagination?: {
        page: number;
        pageSize: number;
    };
    customFilters?: Filters; // custom because not from AntDesign
    sorter?: { [Key in keyof Transaction]?: 'ascend' | 'descend' };
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
    mergeComponent: ({record}: { record: DataType }) => React.ReactNode;
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
    const {dataSource, disabledRows, onRowSelectionChange} = useEntryTableRows({
        data,
        selection,
        onSelectionChange,
    });
    const [tableParams, setTableParams] = useState<TableParams>({
        pagination: {
            page: 1,
            pageSize: 50
        },
    });

    const onFiltersChange = (filters: Filters) => {
        setTableParams(prev => ({
            ...prev,
            customFilters: filters,
        }));
    };

    const onRecordUpdateDebounced = debounce(onRecordUpdate, 250);
    const columns = useEntryTableColumns({
        onCategoryAdd,
        onRecordUpdate: onRecordUpdateDebounced,
        onFiltersChange
    });

    useEffect(() => {
        onChange(tableParams);
    }, [JSON.stringify(tableParams)]); // todo performance and anti-pattern

    const handleTableChange = (
        pagination: TablePaginationConfig,
        filters: Record<string, FilterValue | null>,
        sorterResult: SorterResult<DataType> | SorterResult<DataType>[],
    ) => {
        const sorterResults: SorterResult<DataType>[] = Array.isArray(sorterResult) ? sorterResult : [sorterResult];
        const simplifiedSorter = sorterResults.reduce((prev, curr) => ({
            ...prev,
            [curr.field as string]: curr.order
        }), {} as TableParams['sorter']);

        const simplifiedPagination = (pagination.current !== undefined && pagination.pageSize !== undefined) ? {
            page: pagination.current,
            pageSize: pagination.pageSize
        } : undefined;

        setTableParams(prev => ({
            ...prev,
            sorter: simplifiedSorter,
            pagination: simplifiedPagination,
        }));
    };

    return (
        <>
            <Table
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
                pagination={{
                    ...tableParams.pagination, total: totalEntries,
                    showSizeChanger: true,
                    pageSizeOptions: [50, 100, 500, 1000],
                    position: ['bottomCenter'],
                }}
                onChange={handleTableChange}
                expandable={{
                    showExpandColumn: false,
                    expandedRowRender: (record) => <div>{mergeComponent({record})}</div>,
                    expandedRowKeys: selection.length === 2 ? [selection[0]] : [],
                }}/></>
    );
};
