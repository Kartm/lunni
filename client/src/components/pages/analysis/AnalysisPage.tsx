import React, { useEffect } from "react";
import { useUploadFileToAnalyse } from "../../../hooks/api/useUploadFileToAnalyse";

export const AnalysisPage = () => {
  const {data , mutate} = useUploadFileToAnalyse()
  
  useEffect(() => {
    mutate()
  }, [])

  useEffect(() => {
    data && console.log(data)
  }, [data])
  
  
  return (
    <>

    </>
  );
};
