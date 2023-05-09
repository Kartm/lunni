import { Button, Space, Tag, Typography } from "antd";
import React, { useMemo } from "react";
import { useRematchCategories } from "../../hooks/merger/useRematchCategories";
import { useCategoryStats } from "../../hooks/merger/useCategoryStats";
import { SyncOutlined, RedoOutlined } from "@ant-design/icons";

const { Text } = Typography;

export const RematchCategoriesButton = () => {
  const { mutate, isLoading: isRematchLoading } = useRematchCategories();
  const { data, isLoading: isStatsLoading } = useCategoryStats();

  const missingCategories =
    useMemo(
      () => data?.find((d) => d.categoryName === null)?.totalCount,
      [data]
    ) || 0;

  return (
    <Button
      type="dashed"
      loading={isRematchLoading}
      onClick={() => mutate()}
      icon={<RedoOutlined />}
    >
      Rematch categories ({missingCategories} missing)
    </Button>
  );
};
