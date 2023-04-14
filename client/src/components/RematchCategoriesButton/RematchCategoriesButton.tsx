import { Button, Space } from "antd";
import React from "react";
import { useRematchCategories } from "../../hooks/merger/useRematchCategories";

export const RematchCategoriesButton = () => {
  const { mutate } = useRematchCategories();

  return (
    <Space.Compact>
      <Button
        type="primary"
        onClick={() => {
          mutate();
        }}
      >
        Rematch categories
      </Button>
    </Space.Compact>
  );
};
