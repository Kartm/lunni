import React from "react";
import "./App.css";
import { Layout, Menu } from "antd";
import styled from "styled-components";

const { Header, Content } = Layout;

export const LunniHeader: typeof Header = styled(Header)`
  background-color: #ffffff;
  box-shadow: 0px 3px 15px rgba(0, 0, 0, 0.12);
  display: flex;
  align-items: center;
  justify-content: center;
`;

export const LunniHeaderContent: typeof Header = styled.div`
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 1200px;
`;

export const LunniMenu: typeof Menu = styled(Menu)`
  background-color: #ffffff;
  max-width: 1200px;
`;

export const LunniContent: typeof Content = styled(Content)`
  padding: 50px;
`;

export const LunniLayout: typeof Layout = styled(Layout)`
  min-height: 100vh;
  background-color: #e5e5f7;
  opacity: 0.8;
  background-image: radial-gradient(
    rgba(22, 119, 255, 0.5) 0.5px,
    #e5e5f7 0.5px
  );
  background-size: 10px 10px;
`;

type LunniRouteWrapperProps = {
  background: string;
};
export const LunniRouteWrapper = styled.div<LunniRouteWrapperProps>`
  background: ${(p) => p.background};
  padding: 32px;
  box-shadow: 0px 3px 15px rgba(0, 0, 0, 0.12);
  max-width: 1200px;
  margin: 0 auto;
`;
