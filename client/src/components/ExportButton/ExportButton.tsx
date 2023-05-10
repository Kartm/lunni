import React from "react";
import { DownloadOutlined } from "@ant-design/icons";
import { Button, Select } from "antd";

export const ExportButton = () => (
  <Button
    icon={<DownloadOutlined />}
    href={"http://localhost:8000/api/merger/transactions/export/"}
  >
    Export
  </Button>
);
