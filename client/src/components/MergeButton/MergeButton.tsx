import { Button, InputNumber, Space } from "antd";
import { Key } from "antd/es/table/interface";
import React, { useEffect, useMemo, useState } from "react";
import { Transaction } from "../../models/merger";

type MergeButtonProps = {
  mergeSelection: Key[];
  data: Transaction[];
  onMerge: (sourceId: number, targetId: number, amount: number) => void;
};

export const MergeButton = ({
  mergeSelection,
  data,
  onMerge,
}: MergeButtonProps) => {
  const [value, setValue] = useState<number | null>(0);

  const source = useMemo(
    () =>
      data.find(
        (transaction) =>
          mergeSelection.includes(transaction.id) && transaction.amount > 0
      ),
    [mergeSelection, data]
  );
  const target = useMemo(
    () =>
      data.find(
        (transaction) =>
          mergeSelection.includes(transaction.id) && transaction.amount < 0
      ),
    [mergeSelection, data]
  );

  useEffect(() => {
    if (source) {
      setValue(source.amount);
    } else {
      setValue(null);
    }
  }, [mergeSelection]);

  const handleMergeButton = () => {
    setValue(null);
    onMerge(source!.id, target!.id, value!);
  };

  const numberFormatter = (value?: number) =>
    `PLN ${(parseInt(value?.toString() || "0", 10) / 100).toFixed(2)}`.replace(
      /\B(?=(\d{3})+(?!\d))/g,
      ","
    );

  const numberParser = (value?: string) =>
    parseInt(value!.replace(/\$\s?|(,*)/g, ""), 10) * 100;

  return (
    <Space.Compact>
      <InputNumber
        disabled={!source || !target}
        value={value}
        step={1}
        min={0}
        max={source?.amount}
        onChange={setValue}
        formatter={numberFormatter}
        parser={numberParser}
      />

      <Button
        type="primary"
        disabled={!source || !target || value === 0}
        onClick={() => {
          handleMergeButton();
        }}
      >
        Merge
      </Button>
    </Space.Compact>
  );
};
