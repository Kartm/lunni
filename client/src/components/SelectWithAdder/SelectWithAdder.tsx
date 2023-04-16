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
import { useRematchCategories } from "../../hooks/merger/useRematchCategories";
import { useCategoryStats } from "../../hooks/merger/useCategoryStats";
import { SyncOutlined } from "@ant-design/icons";
import { DataType } from "../EntryTable";
import TextArea from "antd/es/input/TextArea";
import { PlusOutlined } from "@ant-design/icons";
import { SelectProps } from "antd/es/select";

const { Text } = Typography;
const { Option } = Select;

type SelectWithAdderProps = {
  onAddOption: (name: string) => void;
} & SelectProps;

let index = 0;

export const SelectWithAdder = ({
  onAddOption,
  ...props
}: SelectWithAdderProps) => {
  const [name, setName] = useState("");
  const inputRef = useRef<InputRef>(null);

  const onNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setName(event.target.value);
  };

  const addItem = (
    e: React.MouseEvent<HTMLButtonElement | HTMLAnchorElement>
  ) => {
    e.preventDefault();
    onAddOption(name);
    setName("");
    setTimeout(() => {
      inputRef.current?.focus();
    }, 0);
  };

  return (
    <Select
      style={{ width: 300 }}
      placeholder="custom dropdown render"
      dropdownRender={(menu) => (
        <>
          {menu}
          <Divider style={{ margin: "8px 0" }} />
          <Space style={{ padding: "0 8px 4px" }}>
            <Input
              placeholder="Please enter item"
              ref={inputRef}
              value={name}
              onChange={onNameChange}
            />
            <Button type="text" icon={<PlusOutlined />} onClick={addItem}>
              Add item
            </Button>
          </Space>
        </>
      )}
      {...props}
    />
  );
};
