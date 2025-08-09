import React from 'react';
import { Layout as AntLayout, Menu, Avatar, Dropdown } from 'antd';
import { UserOutlined, DashboardOutlined, TeamOutlined, DollarOutlined } from '@ant-design/icons';
import { useNavigate, useLocation } from 'react-router-dom';

const { Header, Sider, Content } = AntLayout;

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const menuItems = [
    {
      key: '/',
      icon: <DashboardOutlined />,
      label: 'Dashboard',
    },
    {
      key: '/employees',
      icon: <TeamOutlined />,
      label: 'Employees',
    },
    {
      key: '/payroll',
      icon: <DollarOutlined />,
      label: 'Payroll',
    },
  ];

  const userMenu = (
    <Menu
      items={[
        { key: 'profile', label: 'Profile' },
        { key: 'settings', label: 'Settings' },
        { key: 'logout', label: 'Logout' },
      ]}
    />
  );

  return (
    <AntLayout style={{ minHeight: '100vh' }}>
      <Sider theme="dark" width={250}>
        <div style={{ padding: '16px', color: 'white', textAlign: 'center' }}>
          <h3>🇲🇾 HRMS Malaysia</h3>
        </div>
        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={({ key }) => navigate(key)}
        />
      </Sider>
      <AntLayout>
        <Header style={{ background: '#fff', padding: '0 24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h2 style={{ margin: 0 }}>Human Resource Management System</h2>
          <Dropdown overlay={userMenu} placement="bottomRight">
            <Avatar icon={<UserOutlined />} style={{ cursor: 'pointer' }} />
          </Dropdown>
        </Header>
        <Content style={{ margin: '24px', background: '#fff', padding: '24px', borderRadius: '8px' }}>
          {children}
        </Content>
      </AntLayout>
    </AntLayout>
  );
};

export default Layout;