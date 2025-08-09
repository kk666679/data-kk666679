import React from 'react';
import { Row, Col, Card, Statistic, Progress, Table } from 'antd';
import { UserOutlined, DollarOutlined, TeamOutlined, TrophyOutlined } from '@ant-design/icons';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const Dashboard: React.FC = () => {
  const monthlyData = [
    { month: 'Jan', employees: 1200, payroll: 2800000 },
    { month: 'Feb', employees: 1220, payroll: 2850000 },
    { month: 'Mar', employees: 1247, payroll: 2900000 },
  ];

  const departmentData = [
    { name: 'IT', value: 35, color: '#1890ff' },
    { name: 'HR', value: 15, color: '#52c41a' },
    { name: 'Finance', value: 20, color: '#faad14' },
    { name: 'Operations', value: 30, color: '#f5222d' },
  ];

  const recentActivities = [
    { key: 1, activity: 'New Employee Onboarded', employee: 'Ahmad Rahman', time: '10:30 AM' },
    { key: 2, activity: 'Leave Request Approved', employee: 'Siti Nurhaliza', time: '11:15 AM' },
    { key: 3, activity: 'Payroll Processed', employee: 'Batch Process', time: '2:45 PM' },
  ];

  return (
    <div>
      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Total Employees"
              value={1247}
              prefix={<UserOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Monthly Payroll"
              value={2900000}
              prefix={<DollarOutlined />}
              valueStyle={{ color: '#52c41a' }}
              formatter={(value) => `RM ${value?.toLocaleString()}`}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Active Departments"
              value={12}
              prefix={<TeamOutlined />}
              valueStyle={{ color: '#faad14' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Employee Satisfaction"
              value={87}
              suffix="%"
              prefix={<TrophyOutlined />}
              valueStyle={{ color: '#f5222d' }}
            />
            <Progress percent={87} showInfo={false} strokeColor="#f5222d" />
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]} style={{ marginTop: 24 }}>
        <Col xs={24} lg={16}>
          <Card title="Employee Growth Trend">
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={monthlyData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="employees" stroke="#1890ff" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </Card>
        </Col>
        <Col xs={24} lg={8}>
          <Card title="Department Distribution">
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={departmentData}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  dataKey="value"
                  label={({ name, value }) => `${name}: ${value}%`}
                >
                  {departmentData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Card>
        </Col>
      </Row>

      <Row style={{ marginTop: 24 }}>
        <Col span={24}>
          <Card title="Recent Activities">
            <Table
              dataSource={recentActivities}
              columns={[
                { title: 'Activity', dataIndex: 'activity', key: 'activity' },
                { title: 'Employee', dataIndex: 'employee', key: 'employee' },
                { title: 'Time', dataIndex: 'time', key: 'time' },
              ]}
              pagination={false}
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;