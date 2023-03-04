import {Button, InputNumber, Space} from "antd";
import {Key} from "antd/es/table/interface";
import React, {useEffect, useMemo, useState} from "react";
import {Transaction} from "../../models/merger";

type MergeButtonProps = {
    mergeSelection: Key[];
    data: Transaction[],
    onMerge: (sourceId: number, targetId: number, amount: number) => void;
}

export const MergeButton = ({mergeSelection, data, onMerge}: MergeButtonProps) => {
    const [value, setValue] = useState<number | null>(null);

    const source = useMemo(
        () => data.find(transaction => mergeSelection.includes(transaction.id) && transaction.amount > 0), [mergeSelection, data])
    const target = useMemo(
        () => data.find(transaction => mergeSelection.includes(transaction.id) && transaction.amount < 0), [mergeSelection, data])

    useEffect(() => {
        if (source) {
            setValue(source.amount / 100);
        } else {
            setValue(null);
        }
    }, [mergeSelection])

    const handleMergeButton = () => {
        setValue(null);
        onMerge(source!.id, target!.id, value!);
    }

    return <Space>
        <InputNumber
            disabled={!source || !target}
            value={value}
            min={1}
            // precision={2}
            max={source?.amount}
            onChange={setValue}
        />
        <Button
            type="ghost"
            onClick={() => {
                setValue(99);
            }}
        >
            Reset
        </Button>
        <Button
            type="primary"
            disabled={!source || !target}
            onClick={() => {
                handleMergeButton()
            }}
        >
            Merge
        </Button>
    </Space>
}