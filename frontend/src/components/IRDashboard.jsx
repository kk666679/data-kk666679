import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Scale, FileText, Users, AlertTriangle, Calendar } from 'lucide-react';

const IRDashboard = () => {
  const [selectedCase, setSelectedCase] = useState(null);
  const [timelineView, setTimelineView] = useState('3d');

  const disputeCases = [
    {
      id: 'DC001',
      type: 'misconduct',
      region: 'KL',
      status: 'active',
      estimatedWeeks: 8,
      progress: 35,
      parties: ['Employee A', 'Management'],
      nextHearing: '2024-02-15'
    },
    {
      id: 'DC002',
      type: 'unfair_dismissal',
      region: 'Johor',
      status: 'mediation',
      estimatedWeeks: 16,
      progress: 60,
      parties: ['Union Rep', 'HR Department'],
      nextHearing: '2024-02-20'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-gray-50 p-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-7xl mx-auto"
      >
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            Industrial Relations Dashboard
          </h1>
          <p className="text-gray-600">
            Malaysian Labor Law Compliance & Dispute Management
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          {[
            { icon: Scale, label: 'Active Cases', value: '12', color: 'blue' },
            { icon: FileText, label: 'Form 32 Generated', value: '8', color: 'green' },
            { icon: Users, label: 'Collective Agreements', value: '3', color: 'purple' },
            { icon: AlertTriangle, label: 'Compliance Alerts', value: '2', color: 'orange' }
          ].map((stat, index) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white p-6 rounded-xl shadow-lg"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 text-sm">{stat.label}</p>
                  <p className="text-2xl font-bold text-gray-800">{stat.value}</p>
                </div>
                <div className={`p-3 rounded-full bg-${stat.color}-100`}>
                  <stat.icon className={`text-${stat.color}-600`} size={24} />
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* 3D Timeline Visualization */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <motion.div
            className="bg-white p-6 rounded-xl shadow-lg"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-semibold">Dispute Case Timeline</h2>
              <div className="flex gap-2">
                <button
                  onClick={() => setTimelineView('3d')}
                  className={`px-3 py-1 rounded ${timelineView === '3d' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
                >
                  3D View
                </button>
                <button
                  onClick={() => setTimelineView('list')}
                  className={`px-3 py-1 rounded ${timelineView === 'list' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
                >
                  List View
                </button>
              </div>
            </div>

            <div className="space-y-4">
              {disputeCases.map((case_, index) => (
                <motion.div
                  key={case_.id}
                  className="border rounded-lg p-4 cursor-pointer hover:shadow-md transition-shadow"
                  whileHover={{ scale: 1.02 }}
                  onClick={() => setSelectedCase(case_)}
                  style={{
                    transform: timelineView === '3d' ? `perspective(1000px) rotateX(${index * 5}deg)` : 'none'
                  }}
                >
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <h3 className="font-semibold">{case_.id}</h3>
                      <p className="text-sm text-gray-600 capitalize">
                        {case_.type.replace('_', ' ')} - {case_.region}
                      </p>
                    </div>
                    <span className={`px-2 py-1 rounded text-xs ${
                      case_.status === 'active' ? 'bg-red-100 text-red-800' :
                      case_.status === 'mediation' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-green-100 text-green-800'
                    }`}>
                      {case_.status}
                    </span>
                  </div>
                  
                  <div className="mb-2">
                    <div className="flex justify-between text-sm mb-1">
                      <span>Progress</span>
                      <span>{case_.progress}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <motion.div
                        className="bg-blue-500 h-2 rounded-full"
                        initial={{ width: 0 }}
                        animate={{ width: `${case_.progress}%` }}
                        transition={{ duration: 1, delay: index * 0.2 }}
                      />
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-2 text-sm text-gray-600">
                    <Calendar size={14} />
                    <span>Next: {case_.nextHearing}</span>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* Case Details Panel */}
          <motion.div
            className="bg-white p-6 rounded-xl shadow-lg"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <h2 className="text-xl font-semibold mb-6">Case Details</h2>
            
            <AnimatePresence mode="wait">
              {selectedCase ? (
                <motion.div
                  key={selectedCase.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className="space-y-4"
                >
                  <div>
                    <h3 className="font-semibold text-lg">{selectedCase.id}</h3>
                    <p className="text-gray-600 capitalize">
                      {selectedCase.type.replace('_', ' ')}
                    </p>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm text-gray-600">Region</p>
                      <p className="font-semibold">{selectedCase.region}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Estimated Duration</p>
                      <p className="font-semibold">{selectedCase.estimatedWeeks} weeks</p>
                    </div>
                  </div>
                  
                  <div>
                    <p className="text-sm text-gray-600 mb-2">Parties Involved</p>
                    <div className="space-y-1">
                      {selectedCase.parties.map((party, index) => (
                        <div key={index} className="flex items-center gap-2">
                          <Users size={16} className="text-gray-400" />
                          <span>{party}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  <div className="pt-4 border-t">
                    <h4 className="font-semibold mb-2">AI Predictions</h4>
                    <div className="bg-blue-50 p-3 rounded-lg">
                      <p className="text-sm">
                        <strong>Success Probability:</strong> 75%
                      </p>
                      <p className="text-sm mt-1">
                        <strong>Recommended Action:</strong> Schedule mediation session
                      </p>
                    </div>
                  </div>
                  
                  <motion.button
                    className="w-full bg-blue-500 text-white py-2 rounded-lg font-semibold"
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    Generate Form 32
                  </motion.button>
                </motion.div>
              ) : (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="text-center text-gray-500 py-12"
                >
                  <Scale size={48} className="mx-auto mb-4 text-gray-300" />
                  <p>Select a case to view details</p>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        </div>

        {/* Collective Agreements Section */}
        <motion.div
          className="mt-8 bg-white p-6 rounded-xl shadow-lg"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <h2 className="text-xl font-semibold mb-6">Collective Agreements</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              {
                union: 'National Union of Bank Employees',
                status: 'active',
                expiry: '2025-12-31',
                compliance: 95
              },
              {
                union: 'Malaysian Trades Union Congress',
                status: 'renewal_due',
                expiry: '2024-06-30',
                compliance: 88
              },
              {
                union: 'Electronics Industry Employees Union',
                status: 'active',
                expiry: '2026-03-15',
                compliance: 92
              }
            ].map((agreement, index) => (
              <motion.div
                key={index}
                className="border rounded-lg p-4"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.4 + index * 0.1 }}
                whileHover={{ y: -5 }}
              >
                <h3 className="font-semibold mb-2">{agreement.union}</h3>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span>Status:</span>
                    <span className={`px-2 py-1 rounded text-xs ${
                      agreement.status === 'active' ? 'bg-green-100 text-green-800' :
                      'bg-yellow-100 text-yellow-800'
                    }`}>
                      {agreement.status.replace('_', ' ')}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span>Expiry:</span>
                    <span>{agreement.expiry}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Compliance:</span>
                    <span className="font-semibold">{agreement.compliance}%</span>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </motion.div>
    </div>
  );
};

export default IRDashboard;