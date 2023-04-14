import { Button, Space, Tag, Typography } from "antd";
import React from "react";
import { useRematchCategories } from "../../hooks/merger/useRematchCategories";
import { useCategoryStats } from "../../hooks/merger/useCategoryStats";
import { SyncOutlined } from "@ant-design/icons";

const { Text } = Typography;

export const RematchCategoriesButton = () => {
  const { mutate, isLoading: isRematchLoading } = useRematchCategories();
  const { data, isLoading: isStatsLoading } = useCategoryStats();

  const label = `${
    data?.find((d) => d.categoryName === null)?.totalCount
  } missing categories`;

  return (
    <Space.Compact>
      <Button
        type="primary"
        loading={isRematchLoading}
        onClick={() => {
          mutate();
        }}
      >
        Rematch categories
      </Button>

      <Tag icon={isStatsLoading && <SyncOutlined spin />} color="processing">
        {data && label}
      </Tag>
    </Space.Compact>
  );
};
