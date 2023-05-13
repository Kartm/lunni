import {
  Button,
  Col,
  Divider,
  Drawer,
  Form,
  Input,
  InputRef,
  Row,
  Select,
  Space,
  Tag,
  Typography,
} from "antd";
import React, { useEffect, useRef, useState } from "react";
import { useRematchCategories } from "../../../hooks/merger/useRematchCategories";
import { useCategoryStats } from "../../../hooks/merger/useCategoryStats";
import { SyncOutlined } from "@ant-design/icons";
import { DataType } from "../../organisms/EntryTable";
import TextArea from "antd/es/input/TextArea";
import { PlusOutlined } from "@ant-design/icons";
import { SelectProps } from "antd/es/select";
import { TransactionCategory } from "../../../models/merger";

const { Text } = Typography;
const { Option } = Select;

type SelectWithAdderProps = {
  onAddOption: (name: string, variant: TransactionCategory["variant"]) => void;
} & Omit<SelectProps, "open">;

export const SelectWithAdder = ({
  onAddOption,
  ...props
}: SelectWithAdderProps) => {
  const [open, setOpen] = useState(false);

  const [newOption, setNewOption] = useState({
    name: "",
    variant: "NEG" as TransactionCategory["variant"],
  });
  const inputRef = useRef<InputRef>(null);

  const onNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setNewOption((old) => ({ ...old, name: event.target.value }));
  };

  const onVariantChange = (variant: TransactionCategory["variant"]) => {
    setNewOption((old) => ({
      ...old,
      variant,
    }));
  };

  const addItem = (
    e: React.MouseEvent<HTMLButtonElement | HTMLAnchorElement>
  ) => {
    e.preventDefault();
    onAddOption(newOption.name, newOption.variant);
    setNewOption({ name: "", variant: "NEG" });

    setTimeout(() => {
      inputRef.current?.focus();
    }, 0);

    setOpen(false);
  };

  return (
    <Select
      {...props}
      open={open}
      onDropdownVisibleChange={(visible) => setOpen(visible)}
      dropdownRender={(menu) => (
        <>
          {menu}
          <Divider style={{ margin: "8px 0" }} />
          <Space style={{ padding: "0 8px 4px" }}>
            <Input
              placeholder="Category name"
              ref={inputRef}
              value={newOption.name}
              onChange={onNameChange}
            />

            <Select
              placeholder="Variant"
              options={["NEG", "POS", "IGN"].map((o) => ({
                label: o,
                value: o,
              }))}
              onChange={onVariantChange}
              onMouseDown={(e) => e.stopPropagation()} // prevent parent Select from closing
            />
          </Space>
          <Button type="text" icon={<PlusOutlined />} onClick={addItem}>
            Add item
          </Button>
        </>
      )}
      {...props}
    />
  );
};
