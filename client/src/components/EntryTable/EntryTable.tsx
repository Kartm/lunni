import React from "react";
import {Table} from "antd";
import {Transaction} from "../../models/merger";

const columns = ['id', 'date', 'description', 'account', 'category', 'amount'].map(c => ({
    title: c,
    dataIndex: c,
    key: c
}));

type EntryTableProps = {
    data: Transaction[];
}

export const EntryTable = ({data}: EntryTableProps) => {

    const dataSource = data.map(d => ({...d, key: d.id}));

    return <Table dataSource={dataSource} columns={columns} />;
}