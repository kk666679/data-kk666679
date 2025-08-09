import React from 'react';
import { Table, Button, Space, Tag, Input, Card } from 'antd';
import { PlusOutlined, SearchOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';

const Employees: React.FC = () => {
  const employees = [
    {
      key: '1',
      employeeId: 'EMP001',
      name: 'Ahmad bin Abdullah',
      ic: '850123-08-1234',
      department: 'IT',
      position: 'Software Engineer',
      salary: 5500,
      status: 'Active',
    },
    {
      key: '2',
      employeeId: 'EMP002',
      name: 'Siti Nurhaliza',
      ic: '900215-14-5678',
      department: 'HR',
      position: 'HR Manager',
      salary: 7200,
      status: 'Active',
    },
    {
      key: '3',
      employeeId: 'EMP003',
      name: 'Lim Wei Ming',
      ic: '880307-07-9012',
      department: 'Finance',
      position: 'Accountant',
      salary: 4800,
      status: 'On Leave',
    },
  ];

  const columns = [
    {
      title: 'Employee ID',
      dataIndex: 'employeeId',
      key: 'employeeId',
    },
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'IC Number',
      dataIndex: 'ic',
      key: 'ic',
    },
    {
      title: 'Department',
      dataIndex: 'department',
      key: 'department',
    },
    {
      title: 'Position',
      dataIndex: 'position',
      key: 'position',
    },
    {
      title: 'Salary',
      dataIndex: 'salary',
      key: 'salary',
      render: (salary: number) => `RM ${salary.toLocaleString()}`,
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <Tag color={status === 'Active' ? 'green' : status === 'On Leave' ? 'orange' : 'red'}>
          {status}
        </Tag>
      ),
    },
    {
      title: 'Actions',
      key: 'actions',
      render: () => (
        <Space>
          <Button type="link" icon={<EditOutlined />} size="small">
            Edit
          </Button>
          <Button type="link" danger icon={<DeleteOutlined />} size="small">
            Delete
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <Card>
      <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between' }}>
        <Input
          placeholder="Search employees..."
          prefix={<SearchOutlined />}
          style={{ width: 300 }}
        />
        <Button type="primary" icon={<PlusOutlined />}>
          Add Employee
        </Button>
      </div>
      <Table
        columns={columns}
        dataSource={employees}
        pagination={{
          total: employees.length,
          pageSize: 10,
          showSizeChanger: true,
          showQuickJumper: true,
        }}
      />
    </Card>
  );
};

export default Employees;