import React from "react";
import { DownloadOutlined } from "@ant-design/icons";
import { Button } from "antd";
import { useUploadFileToAnalyse } from "../../../hooks/api/useUploadFileToAnalyse";
import { Link } from "react-router-dom";

export const AnalyseButton = () => (<Link to={'/analysis'}>
  <Button>
    Analyse
  </Button>
</Link>
)

