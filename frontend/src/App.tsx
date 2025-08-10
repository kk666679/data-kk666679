import { Suspense, lazy } from 'react'
import { Routes, Route } from 'react-router-dom'
import { Spin } from 'antd'
import { Layout } from 'antd'
import { useState } from 'react'

const { Header, Content } = Layout

// Lazy load pages for better performance
const Dashboard = lazy(() => import('./pages/Dashboard'))

export default function App() {
  const [collapsed, setCollapsed] = useState(false)

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ padding: 0, background: '#fff' }}>
        <div style={{ color: '#000', fontSize: 18, padding: '0 16px' }}>
          HRMS Dashboard
        </div>
      </Header>
      
      <Layout>
        <Content style={{ margin: '24px 16px', padding: 24, minHeight: 280 }}>
          <Suspense fallback={
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
              <Spin size="large" />
            </div>
          }>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/dashboard" element={<Dashboard />} />
            </Routes>
          </Suspense>
        </Content>
      </Layout>
    </Layout>
  )
}
