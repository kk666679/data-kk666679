import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, AlertCircle, Clock } from 'lucide-react';

const ComplianceStatus = () => {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch compliance status from API
    fetch('/api/compliance-status')
      .then(res => res.json())
      .then(data => {
        setStatus(data);
        setLoading(false);
      })
      .catch(() => {
        // Mock data for demo
        setStatus({
          epf: true,
          socso: true,
          employment_act: "2024-01-15",
          pdpa: true,
          updated_at: new Date().toISOString()
        });
        setLoading(false);
      });
  }, []);

  const complianceItems = [
    { key: 'epf', label: 'EPF Compliance', description: '11% Employee, 13% Employer' },
    { key: 'socso', label: 'SOCSO Integration', description: 'Automated contributions' },
    { key: 'pdpa', label: 'PDPA 2010', description: 'Data protection compliant' },
    { key: 'employment_act', label: 'Employment Act 1955', description: 'Latest updates applied' }
  ];

  if (loading) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <motion.div
          className="flex items-center justify-center h-32"
          animate={{ rotate: 360 }}
          transition={{ repeat: Infinity, duration: 1 }}
        >
          <Clock className="text-blue-500" size={32} />
        </motion.div>
      </div>
    );
  }

  return (
    <motion.div
      className="bg-white p-6 rounded-lg shadow-lg"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <h3 className="text-xl font-semibold mb-4 text-gray-800">Live Compliance Status</h3>
      
      <div className="space-y-4">
        {complianceItems.map((item, index) => {
          const isCompliant = status[item.key] === true || 
                             (item.key === 'employment_act' && status[item.key]);
          
          return (
            <motion.div
              key={item.key}
              className="flex items-center justify-between p-3 rounded-lg bg-gray-50"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <div className="flex items-center gap-3">
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: index * 0.1 + 0.3, type: "spring" }}
                >
                  {isCompliant ? (
                    <CheckCircle className="text-green-500" size={24} />
                  ) : (
                    <AlertCircle className="text-yellow-500" size={24} />
                  )}
                </motion.div>
                
                <div>
                  <h4 className="font-medium text-gray-800">{item.label}</h4>
                  <p className="text-sm text-gray-600">{item.description}</p>
                </div>
              </div>
              
              <motion.div
                className={`px-3 py-1 rounded-full text-sm font-medium ${
                  isCompliant 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-yellow-100 text-yellow-800'
                }`}
                whileHover={{ scale: 1.05 }}
              >
                {isCompliant ? 'Active' : 'Pending'}
              </motion.div>
            </motion.div>
          );
        })}
      </div>
      
      <motion.div
        className="mt-4 text-xs text-gray-500 text-center"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8 }}
      >
        Last updated: {new Date(status.updated_at).toLocaleString()}
      </motion.div>
    </motion.div>
  );
};

export default ComplianceStatus;