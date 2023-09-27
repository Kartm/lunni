import React, { useEffect, useState } from 'react';
import { Table, TablePaginationConfig } from 'antd';
import { Transaction } from '../../../models/merger';
import { FilterValue, Key, SorterResult } from 'antd/es/table/interface';
import { TransactionPartial } from '../../../api/merger';
import { debounce } from 'lodash';
import { useEntryTableColumns, useEntryTableRows } from '../../../hooks/components';

export type DataType = Transaction & {
    key: Key;
};

export type TableParams = {
    pagination?: TablePaginationConfig;
    filters?: Record<string, FilterValue | null>;
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
            pagination: { ...prev.pagination, ...pagination },
            filters: { ...prev.filters, ...filters },
            sorter: { ...prev.sorter, ...sorter },
        }));
    };

    return (
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
            pagination={tableParams.pagination}
            onChange={handleTableChange}
            expandable={{
                showExpandColumn: false,
                expandedRowRender: (record) => <div>{mergeComponent({ record })}</div>,
                expandedRowKeys: selection.length === 2 ? [selection[0]] : [],
            }}
        />
    );
};
