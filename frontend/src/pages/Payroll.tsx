import React from 'react';
import { Card, Row, Col, Statistic, Table, Button, Tag, Space } from 'antd';
import { DollarOutlined, BankOutlined, FileTextOutlined } from '@ant-design/icons';

const Payroll: React.FC = () => {
  const payrollData = [
    {
      key: '1',
      employeeId: 'EMP001',
      name: 'Ahmad bin Abdullah',
      basicSalary: 5500,
      epfEmployee: 605,
      epfEmployer: 715,
      socsoEmployee: 27.5,
      socsoEmployer: 96.25,
      netSalary: 4867.5,
      status: 'Processed',
    },
    {
      key: '2',
      employeeId: 'EMP002',
      name: 'Siti Nurhaliza',
      basicSalary: 7200,
      epfEmployee: 792,
      epfEmployer: 936,
      socsoEmployee: 36,
      socsoEmployer: 126,
      netSalary: 6372,
      status: 'Processed',
    },
  ];

  const columns = [
    {
      title: 'Employee',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Basic Salary',
      dataIndex: 'basicSalary',
      key: 'basicSalary',
      render: (amount: number) => `RM ${amount.toLocaleString()}`,
    },
    {
      title: 'EPF Employee',
      dataIndex: 'epfEmployee',
      key: 'epfEmployee',
      render: (amount: number) => `RM ${amount.toLocaleString()}`,
    },
    {
      title: 'SOCSO Employee',
      dataIndex: 'socsoEmployee',
      key: 'socsoEmployee',
      render: (amount: number) => `RM ${amount.toLocaleString()}`,
    },
    {
      title: 'Net Salary',
      dataIndex: 'netSalary',
      key: 'netSalary',
      render: (amount: number) => `RM ${amount.toLocaleString()}`,
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <Tag color={status === 'Processed' ? 'green' : 'orange'}>
          {status}
        </Tag>
      ),
    },
    {
      title: 'Actions',
      key: 'actions',
      render: () => (
        <Space>
          <Button type="link" icon={<FileTextOutlined />} size="small">
            Payslip
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={8}>
          <Card>
            <Statistic
              title="Total Payroll"
              value={2900000}
              prefix={<DollarOutlined />}
              valueStyle={{ color: '#1890ff' }}
              formatter={(value) => `RM ${value?.toLocaleString()}`}
            />
          </Card>
        </Col>
        <Col xs={24} sm={8}>
          <Card>
            <Statistic
              title="EPF Contributions"
              value={312000}
              prefix={<BankOutlined />}
              valueStyle={{ color: '#52c41a' }}
              formatter={(value) => `RM ${value?.toLocaleString()}`}
            />
          </Card>
        </Col>
        <Col xs={24} sm={8}>
          <Card>
            <Statistic
              title="SOCSO Contributions"
              value={45000}
              prefix={<BankOutlined />}
              valueStyle={{ color: '#faad14' }}
              formatter={(value) => `RM ${value?.toLocaleString()}`}
            />
          </Card>
        </Col>
      </Row>

      <Card title="Monthly Payroll - December 2024">
        <Table
          columns={columns}
          dataSource={payrollData}
          pagination={false}
          summary={(pageData) => {
            let totalBasic = 0;
            let totalNet = 0;
            
            pageData.forEach(({ basicSalary, netSalary }) => {
              totalBasic += basicSalary;
              totalNet += netSalary;
            });

            return (
              <Table.Summary.Row>
                <Table.Summary.Cell index={0}><strong>Total</strong></Table.Summary.Cell>
                <Table.Summary.Cell index={1}>
                  <strong>RM {totalBasic.toLocaleString()}</strong>
                </Table.Summary.Cell>
                <Table.Summary.Cell index={2}>-</Table.Summary.Cell>
                <Table.Summary.Cell index={3}>-</Table.Summary.Cell>
                <Table.Summary.Cell index={4}>
                  <strong>RM {totalNet.toLocaleString()}</strong>
                </Table.Summary.Cell>
                <Table.Summary.Cell index={5}>-</Table.Summary.Cell>
                <Table.Summary.Cell index={6}>-</Table.Summary.Cell>
              </Table.Summary.Row>
            );
          }}
        />
      </Card>
    </div>
  );
};

export default Payroll;