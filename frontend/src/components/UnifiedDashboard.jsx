import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import useSWR from 'swr';

const fetcher = (url) => fetch(url).then(res => res.json());

const UnifiedDashboard = () => {
  const { data: dashboardData, error } = useSWR('/api/dashboard', fetcher, { refreshInterval: 5000 });
  const [selectedModule, setSelectedModule] = useState('overview');

  if (error) return <div>Failed to load dashboard</div>;
  if (!dashboardData) return <div>Loading...</div>;

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-7xl mx-auto"
      >
        <h1 className="text-3xl font-bold mb-8">HRMS Malaysia - Unified Dashboard</h1>

        {/* Module Selector */}
        <div className="flex gap-4 mb-8">
          {['overview', 'ir', 'er', 'ta', 'ld', 'payroll'].map(module => (
            <motion.button
              key={module}
              onClick={() => setSelectedModule(module)}
              className={`px-4 py-2 rounded-lg font-semibold ${
                selectedModule === module ? 'bg-blue-500 text-white' : 'bg-white'
              }`}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              {module.toUpperCase()}
            </motion.button>
          ))}
        </div>

        {/* Dashboard Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* IR Module */}
          <motion.div
            className="bg-white p-6 rounded-xl shadow-lg"
            whileHover={{ scale: 1.02 }}
          >
            <h2 className="text-xl font-semibold mb-4">Industrial Relations</h2>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span>Active Cases</span>
                <span className="font-bold text-red-600">{dashboardData.ir?.active_cases || 12}</span>
              </div>
              <div className="flex justify-between">
                <span>Form 32 Generated</span>
                <span className="font-bold text-green-600">{dashboardData.ir?.forms_generated || 8}</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <motion.div
                  className="bg-blue-500 h-2 rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: '75%' }}
                  transition={{ duration: 1 }}
                />
              </div>
            </div>
          </motion.div>

          {/* ER Sentiment Heatmap */}
          <motion.div
            className="bg-white p-6 rounded-xl shadow-lg"
            whileHover={{ scale: 1.02 }}
          >
            <h2 className="text-xl font-semibold mb-4">Employee Relations</h2>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={dashboardData.er?.department_sentiment || []}>
                <XAxis dataKey="department" />
                <YAxis />
                <Bar dataKey="score" fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
          </motion.div>

          {/* Payroll Compliance */}
          <motion.div
            className="bg-white p-6 rounded-xl shadow-lg"
            whileHover={{ scale: 1.02 }}
          >
            <h2 className="text-xl font-semibold mb-4">Payroll Compliance</h2>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span>EPF Compliance</span>
                <span className="text-green-600">✓ 100%</span>
              </div>
              <div className="flex justify-between">
                <span>SOCSO Compliance</span>
                <span className="text-green-600">✓ 100%</span>
              </div>
              <div className="flex justify-between">
                <span>Monthly Payroll</span>
                <span className="font-bold">RM {dashboardData.payroll?.monthly_total || '750K'}</span>
              </div>
            </div>
          </motion.div>

          {/* TA Recruitment Funnel */}
          <motion.div
            className="bg-white p-6 rounded-xl shadow-lg col-span-2"
            whileHover={{ scale: 1.01 }}
          >
            <h2 className="text-xl font-semibold mb-4">Talent Acquisition Pipeline</h2>
            <div className="flex justify-between items-center">
              {['Applications', 'Screened', 'Interviewed', 'Hired'].map((stage, index) => (
                <motion.div
                  key={stage}
                  className="text-center"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.2 }}
                >
                  <div className={`w-16 h-16 rounded-full flex items-center justify-center text-white font-bold ${
                    index === 0 ? 'bg-blue-500' :
                    index === 1 ? 'bg-green-500' :
                    index === 2 ? 'bg-yellow-500' : 'bg-purple-500'
                  }`}>
                    {dashboardData.ta?.funnel?.[stage.toLowerCase()] || [150, 75, 30, 8][index]}
                  </div>
                  <p className="mt-2 text-sm">{stage}</p>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* L&D HRDF Claims */}
          <motion.div
            className="bg-white p-6 rounded-xl shadow-lg"
            whileHover={{ scale: 1.02 }}
          >
            <h2 className="text-xl font-semibold mb-4">HRDF Claims</h2>
            <ResponsiveContainer width="100%" height={200}>
              <PieChart>
                <Pie
                  data={[
                    { name: 'Approved', value: 60, fill: '#00C49F' },
                    { name: 'Pending', value: 30, fill: '#FFBB28' },
                    { name: 'Rejected', value: 10, fill: '#FF8042' }
                  ]}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  dataKey="value"
                />
              </PieChart>
            </ResponsiveContainer>
          </motion.div>
        </div>

        {/* Real-time Updates */}
        <motion.div
          className="mt-8 bg-white p-6 rounded-xl shadow-lg"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          <h2 className="text-xl font-semibold mb-4">Real-time Updates</h2>
          <div className="space-y-2">
            <div className="flex items-center gap-3">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-sm">New EPF calculation completed for 15 employees</span>
              <span className="text-xs text-gray-500">2 min ago</span>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
              <span className="text-sm">IR case DC001 moved to mediation phase</span>
              <span className="text-xs text-gray-500">5 min ago</span>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-2 h-2 bg-yellow-500 rounded-full animate-pulse"></div>
              <span className="text-sm">HRDF claim HRDF-002 approved - RM 2,500</span>
              <span className="text-xs text-gray-500">8 min ago</span>
            </div>
          </div>
        </motion.div>
      </motion.div>
    </div>
  );
};

export default UnifiedDashboard;