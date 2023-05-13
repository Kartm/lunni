import { InputNumber, Slider } from "antd";
import React, { useEffect, useState } from "react";

type InputMoneyProps = {
  min: number;
  max: number;
  value: number | null;
  setValue: (newValue: number | null) => void;
};

// Assumes that money is stored as cents, not a decimal
export const InputMoney = ({ min, max, value, setValue }: InputMoneyProps) => {
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
    <>
      <Slider
        min={min}
        max={max}
        onChange={onChange}
        value={typeof value === "number" ? value : 0}
        style={{ width: 200 }}
        tooltip={{ formatter: formatMoney }}
      />

      <InputNumber
        value={value}
        min={min}
        max={max}
        onChange={onChange}
        formatter={formatMoney}
        parser={parseMoney}
      />
    </>
  );
};
