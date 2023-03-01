import React from "react";
import {Table} from "antd";
import {Transaction} from "../../models/merger";

const dataSource = [
    {
        key: '1',
        name: 'Mike',
        age: 32,
        address: '10 Downing Street',
    },
    {
        key: '2',
        name: 'John',
        age: 42,
        address: '10 Downing Street',
    },
];

const columns = [
    {
        title: 'Name',
        dataIndex: 'name',
        key: 'name',
    },
    {
        title: 'Age',
        dataIndex: 'age',
        key: 'age',
    },
    {
        title: 'Address',
        dataIndex: 'address',
        key: 'address',
    },
];

type EntryTableProps = {
    data: Transaction[];
}

export const EntryTable = ({data}: EntryTableProps) => {
    console.log(data)
    return <Table dataSource={dataSource} columns={columns} />;
}