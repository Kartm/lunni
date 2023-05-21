import { Button, Divider, Typography } from "antd";
import { useNavigate } from "react-router-dom";
import { routes } from "../../../config/routes";
import { ArrowRightOutlined } from "@ant-design/icons";

const { Title, Paragraph } = Typography;

export const HomePage = () => {
  const navigate = useNavigate();

  return (
    <>
      <Title level={2}>Lunni - a tool for managing personal finance.</Title>

      <Paragraph>
        If you frequently make shared orders with friends or utilize many bank
        accounts, then Lunni can help you to better organize and analyze your
        finance data.
      </Paragraph>

      <div style={{ height: "32px" }}></div>

      <Button type="primary" onClick={() => navigate(Object.keys(routes)[1])}>
        Get started
        <ArrowRightOutlined />
      </Button>
    </>
  );
};
