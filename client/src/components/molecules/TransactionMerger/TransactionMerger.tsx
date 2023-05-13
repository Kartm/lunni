import { Button, InputNumber, Slider, Space } from "antd";
import { Key } from "antd/es/table/interface";
import React, { useEffect, useMemo, useState } from "react";
import { Transaction } from "../../../models/merger";
import { InputMoney } from "../../atoms/InputMoney";

type MergeButtonProps = {
  mergeSelection: Key[];
  data: Transaction[];
  onMerge: (sourceId: number, targetId: number, amount: number) => void;
};

export const TransactionMerger = ({
  mergeSelection,
  data,
  onMerge,
}: MergeButtonProps) => {
  const [value, setValue] = useState<number | null>(0);

  const [source, target] = useMemo(
    () => [
      data.find((transaction) => transaction.id === mergeSelection[0]),
      data.find((transaction) => transaction.id === mergeSelection[1]),
    ],
    [mergeSelection, data]
  );

  const [min, max] = useMemo(() => [0, source?.amount || 0], [source]);

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

  return (
    <Space>
      <InputMoney
        min={min}
        max={max}
        value={value}
        setValue={(newValue) => setValue(newValue)}
      />
      <Button type="primary" onClick={() => handleMergeButton()}>
        Merge
      </Button>
    </Space>
  );
};
