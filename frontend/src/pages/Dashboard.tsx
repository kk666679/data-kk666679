import { useState, useEffect } from 'react'
import { Card, Col, Row, Statistic, Typography } from 'antd'
import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'

const { Title } = Typography

// Mock API call
const fetchDashboardData = async () => {
  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 1000))
  return {
    totalEmployees: 1250,
    activeProjects: 42,
    pendingTasks: 89,
    completedTasks: 1567,
  }
}

export default function Dashboard() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['dashboard'],
    queryFn: fetchDashboardData,
  })

  if (error) return <div>Error loading dashboard data</div>

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Title level={2}>Dashboard</Title>
      
      <Row gutter={[16, 16]} style={{ marginTop: 24 }}>
        <Col xs={24} sm={12} lg={6}>
          <Card loading={isLoading}>
            <Statistic
              title="Total Employees"
              value={data?.totalEmployees || 0}
              valueStyle={{ color: '#3f8600' }}
            />
          </Card>
        </Col>
        
        <Col xs={24} sm={12} lg={6}>
          <Card loading={isLoading}>
            <Statistic
              title="Active Projects"
              value={data?.activeProjects || 0}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        
        <Col xs={24} sm={12} lg={6}>
          <Card loading={isLoading}>
            <Statistic
              title="Pending Tasks"
              value={data?.pendingTasks || 0}
              valueStyle={{ color: '#faad14' }}
            />
          </Card>
        </Col>
        
        <Col xs={24} sm={12} lg={6}>
          <Card loading={isLoading}>
            <Statistic
              title="Completed Tasks"
              value={data?.completedTasks || 0}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
      </Row>
    </motion.div>
  )
}
