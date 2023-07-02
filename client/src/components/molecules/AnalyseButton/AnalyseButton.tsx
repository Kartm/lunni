import React from "react";
import { DownloadOutlined } from "@ant-design/icons";
import { Button } from "antd";
import { useUploadFileToAnalyse } from "../../../hooks/api/useUploadFileToAnalyse";

export const AnalyseButton = () => {
  const {mutate} = useUploadFileToAnalyse()
  return <Button onClick={() => mutate()}>
    Analyse
  </Button>
}

