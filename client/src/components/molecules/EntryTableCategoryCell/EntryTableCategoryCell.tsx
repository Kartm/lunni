import { Button, Typography } from "antd";
import React from "react";
import { PlusCircleOutlined } from "@ant-design/icons";
import { Transaction } from "../../../models/merger";

const { Text } = Typography;

type EntryTableCategoryCellProps = {
  category?: Transaction["category"];
  onClickAdd: () => void;
};

export const EntryTableCategoryCell = ({
  category,
  onClickAdd,
}: EntryTableCategoryCellProps) => (
  <Text
    type={
      category?.variant === "POS"
        ? "success"
        : category?.variant === "NEG"
        ? "danger"
        : "secondary"
    }
  >
    {category?.name || (
      <Button
        icon={<PlusCircleOutlined />}
        size={"small"}
        type={"ghost"}
        title={"Category is missing"}
        onClick={() => onClickAdd()}
      />
    )}
  </Text>
);
