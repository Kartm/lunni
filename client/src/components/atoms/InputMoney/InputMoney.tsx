import { InputNumber, Slider } from "antd";
import React from "react";
import { formatMoney, parseMoney } from "./InputMoney.utils";

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
