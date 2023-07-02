import React, { useEffect, useState } from "react";
import { useUploadFileToAnalyse } from "../../../hooks/api/useUploadFileToAnalyse";
import { Chart, registerables } from 'chart.js'
import { Bar } from "react-chartjs-2";
import { Button, Empty } from "antd";
import { Link } from "react-router-dom";


export const AnalysisPage = () => {
  const { data, mutate } = useUploadFileToAnalyse()
  const [options, setOptions] = useState({});
  const [graphData, setGraphData] = useState<any>({
    datasets: []
  });

  Chart.register(...registerables)

  useEffect(() => {
    mutate()
  }, [])

  useEffect(() => {
    data && prepareGraph(data)
  }, [data])

  const prepareGraph = (jsonData: any) => {
    const categories = [...new Set(jsonData.map((item: any) => item.category_name))];
    const months = [...new Set(jsonData.map((item: any) => item.month))];

    const labels = months;

    const datasets = categories.map(category => {
      const categoryData = jsonData
        .filter((item: any) => item.category_name === category)
        .map((item: any) => item.calculated_amount);

      const randomColor = `rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(
        Math.random() * 256
      )}, ${Math.floor(Math.random() * 256)}, 0.5)`;

      return {
        label: category,
        data: categoryData,
        backgroundColor: randomColor,
      };
    });

    const options = {
      plugins: {
        title: {
          display: true,
          text: 'Your expenses per month',
        },
      },
      responsive: true,
      scales: {
        x: {
          stacked: true,
        },
        y: {
          stacked: true,
        },
      },
    };

    const data = {
      labels: labels,
      datasets: datasets,
    };

    setOptions(options)
    setGraphData(data)
  }

  return (
    <>
      {data && !data.length ?
        <Empty>
          <Link to={'/merger'}>
            <Button type="primary">Upload data</Button>
          </Link>
        </Empty>
        :
        <Bar options={options} data={graphData} />
      }
    </>
  );
};
