import { Button, Col, InputNumber, Row, Slider, Space } from "antd";
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

  const [source, target] = useMemo(
    () => [
      data.find((transaction) => transaction.id === mergeSelection[0]),
      data.find((transaction) => transaction.id === mergeSelection[1]),
    ],
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

  const onChange = (newValue: number | null) => {
    setValue(newValue);
  };

  const formatMoney = (value?: number) => {
    if (!value) return "";
    return (value / 100).toFixed(2);
  };

  const parseMoney = (value?: string) => {
    if (!value) return 0;
    const numericValue = parseFloat(value);
    const intValue = Math.round(numericValue * 100);
    return isNaN(intValue) ? 0 : intValue;
  };

  return (
    <Space>
      <Slider
        disabled={!source || !target}
        min={0}
        max={source?.amount}
        onChange={onChange}
        value={typeof value === "number" ? value : 0}
        style={{ width: 200 }}
        tooltip={{ formatter: formatMoney }}
      />
      <InputNumber
        disabled={!source || !target}
        value={value}
        min={0}
        max={source?.amount}
        onChange={onChange}
        formatter={formatMoney}
        parser={parseMoney}
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
    </Space>
  );
};
