import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Scale, Users, Calculator, BookOpen, Home } from 'lucide-react';
import IRDashboard from './IRDashboard';
import ERDashboard from './ERDashboard';
import PayrollDashboard from './PayrollDashboard';
import LDDashboard from './LDDashboard';

const MainDashboard = () => {
  const [activeModule, setActiveModule] = useState('home');

  const modules = [
    { id: 'home', name: 'Overview', icon: Home, color: 'blue' },
    { id: 'ir', name: 'Industrial Relations', icon: Scale, color: 'purple' },
    { id: 'er', name: 'Employee Relations', icon: Users, color: 'green' },
    { id: 'payroll', name: 'Payroll', icon: Calculator, color: 'orange' },
    { id: 'ld', name: 'Learning & Development', icon: BookOpen, color: 'indigo' }
  ];

  const renderModule = () => {
    switch(activeModule) {
      case 'ir': return <IRDashboard />;
      case 'er': return <ERDashboard />;
      case 'payroll': return <PayrollDashboard />;
      case 'ld': return <LDDashboard />;
      default: return <HomeOverview />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="fixed left-0 top-0 h-full w-64 bg-white shadow-lg z-10">
        <div className="p-6">
          <h1 className="text-2xl font-bold text-gray-800">HRMS Malaysia</h1>
          <p className="text-sm text-gray-600">AI-Powered HR Management</p>
        </div>
        
        <nav className="mt-8">
          {modules.map((module) => (
            <motion.button
              key={module.id}
              onClick={() => setActiveModule(module.id)}
              className={`w-full flex items-center gap-3 px-6 py-3 text-left transition-colors ${
                activeModule === module.id 
                  ? `bg-${module.color}-50 text-${module.color}-700 border-r-4 border-${module.color}-500` 
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
              whileHover={{ x: 5 }}
              whileTap={{ scale: 0.98 }}
            >
              <module.icon size={20} />
              <span className="font-medium">{module.name}</span>
            </motion.button>
          ))}
        </nav>
      </div>

      {/* Main Content */}
      <div className="ml-64">
        <motion.div
          key={activeModule}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.3 }}
        >
          {renderModule()}
        </motion.div>
      </div>
    </div>
  );
};

const HomeOverview = () => (
  <div className="p-6">
    <h1 className="text-3xl font-bold mb-8">HRMS Overview</h1>
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {[
        { title: 'Active Employees', value: '150', color: 'blue' },
        { title: 'Pending Cases', value: '12', color: 'red' },
        { title: 'Monthly Payroll', value: 'RM 750K', color: 'green' },
        { title: 'Training Hours', value: '2,340', color: 'purple' }
      ].map((stat, index) => (
        <motion.div
          key={stat.title}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
          className="bg-white p-6 rounded-xl shadow-lg"
        >
          <h3 className="text-sm text-gray-600">{stat.title}</h3>
          <p className={`text-3xl font-bold text-${stat.color}-600`}>{stat.value}</p>
        </motion.div>
      ))}
    </div>
  </div>
);

export default MainDashboard;