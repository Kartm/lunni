import React from "react";
import { BankStatementUploadModal } from "../../molecules/BankStatementUploadModal";
import { RematchCategoriesButton } from "../../molecules/RematchCategoriesButton";
import { Space } from "antd";
import { ExportButton } from "../../molecules/ExportButton";
import { AnalyseButton } from "../../molecules/AnalyseButton";

export const MergerPageActions = () => {
  return (
    <Space>
      <BankStatementUploadModal />

      <RematchCategoriesButton />

      <ExportButton />

      <AnalyseButton />
    </Space>
  );
};
