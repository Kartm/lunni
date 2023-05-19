import React from "react";
import "./App.css";
import { Link, Route, Routes, useLocation } from "react-router-dom";
import { Layout, Menu, theme } from "antd";
import { routes } from "./config/routes";

const { Header, Content } = Layout;

const App = () => {
  const {
    token: { colorBgContainer },
  } = theme.useToken();
  const location = useLocation();

  return (
    <Layout className="layout" style={{ minHeight: "100vh" }}>
      <Header>
        <Menu
          theme="dark"
          mode="horizontal"
          defaultSelectedKeys={[location.pathname]}
          items={Object.entries(routes).map(([path, details]) => ({
            key: path,
            label: <Link to={path}>{details.title}</Link>,
          }))}
        />
      </Header>
      <Content style={{ padding: "50px" }}>
        <div
          className="site-layout-content"
          style={{ background: colorBgContainer }}
        >
          <Routes>
            {Object.entries(routes).map(([path, details]) => (
              <Route key={path} path={path} element={details.component} />
            ))}
          </Routes>
        </div>
      </Content>
    </Layout>
  );
};

export default App;
