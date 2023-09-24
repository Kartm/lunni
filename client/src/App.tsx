import React from 'react';
import './App.css';
import { Link, Route, Routes, useLocation } from 'react-router-dom';
import { theme } from 'antd';
import { routes } from './config/routes';
import {
    LunniContent,
    LunniHeader,
    LunniHeaderContent,
    LunniLayout,
    LunniMenu,
    LunniRouteWrapper,
} from './App.styles';
import { LunniLogo } from './components/atoms/LunniLogo';

const App = () => {
    const {
        token: { colorBgContainer },
    } = theme.useToken();
    const location = useLocation();

    return (
        <LunniLayout>
            <LunniHeader>
                <LunniHeaderContent>
                    <LunniLogo $size={32} />
                    <LunniMenu
                        theme='light'
                        mode='horizontal'
                        selectedKeys={[location.pathname]}
                        items={Object.entries(routes).map(([path, details]) => ({
                            key: path,
                            label: <Link to={path}>{details.title}</Link>,
                        }))}
                    />
                </LunniHeaderContent>
            </LunniHeader>
            <LunniContent>
                <LunniRouteWrapper background={colorBgContainer}>
                    <Routes>
                        {Object.entries(routes).map(([path, details]) => (
                            <Route key={path} path={path} element={details.component} />
                        ))}
                    </Routes>
                </LunniRouteWrapper>
            </LunniContent>
        </LunniLayout>
    );
};

export default App;
