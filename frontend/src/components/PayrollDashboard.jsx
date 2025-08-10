import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Calculator, FileText, TrendingUp, Users, Download, Eye } from 'lucide-react';

const PayrollDashboard = () => {
  const [selectedEmployee, setSelectedEmployee] = useState(null);
  const [payrollData, setPayrollData] = useState(null);
  const [calculationMode, setCalculationMode] = useState('single');

  const employees = [
    { id: 'EMP001', name: 'Ahmad Rahman', salary: 5000, type: 'local' },
    { id: 'EMP002', name: 'Lim Wei Ming', salary: 6500, type: 'local' },
    { id: 'EMP003', name: 'Priya Devi', salary: 4200, type: 'local' },
    { id: 'EMP004', name: 'John Smith', salary: 8000, type: 'foreign' }
  ];

  const calculatePayroll = async (employee) => {
    const response = await fetch('/api/payroll/calculate/full', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        employee_id: employee.id,
        basic_salary: employee.salary,
        allowances: 500,
        overtime: 200,
        bonus: 1000,
        employee_type: employee.type
      })
    });
    
    if (response.ok) {
      const data = await response.json();
      setPayrollData(data);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 p-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-7xl mx-auto"
      >
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            Malaysian Payroll System
          </h1>
          <p className="text-gray-600">
            EPF • SOCSO • EIS • PCB Compliant Calculations
          </p>
        </div>

        {/* Mode Toggle */}
        <div className="mb-6">
          <div className="flex gap-2">
            <button
              onClick={() => setCalculationMode('single')}
              className={`px-4 py-2 rounded-lg font-semibold ${
                calculationMode === 'single' 
                  ? 'bg-green-500 text-white' 
                  : 'bg-white text-gray-700'
              }`}
            >
              Single Employee
            </button>
            <button
              onClick={() => setCalculationMode('bulk')}
              className={`px-4 py-2 rounded-lg font-semibold ${
                calculationMode === 'bulk' 
                  ? 'bg-green-500 text-white' 
                  : 'bg-white text-gray-700'
              }`}
            >
              Bulk Processing
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Employee Selection */}
          <motion.div
            className="bg-white p-6 rounded-xl shadow-lg"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <h2 className="text-xl font-semibold mb-6">Select Employee</h2>
            
            <div className="space-y-3">
              {employees.map((employee, index) => (
                <motion.div
                  key={employee.id}
                  className={`p-4 rounded-lg border cursor-pointer transition-all ${
                    selectedEmployee?.id === employee.id 
                      ? 'border-green-500 bg-green-50' 
                      : 'border-gray-200 hover:border-green-300'
                  }`}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  whileHover={{ scale: 1.02 }}
                  onClick={() => {
                    setSelectedEmployee(employee);
                    calculatePayroll(employee);
                  }}
                >
                  <div className="flex justify-between items-center">
                    <div>
                      <h3 className="font-semibold">{employee.name}</h3>
                      <p className="text-sm text-gray-600">{employee.id}</p>
                    </div>
                    <div className="text-right">
                      <p className="font-semibold">RM {employee.salary.toLocaleString()}</p>
                      <span className={`text-xs px-2 py-1 rounded ${
                        employee.type === 'local' 
                          ? 'bg-blue-100 text-blue-800' 
                          : 'bg-orange-100 text-orange-800'
                      }`}>
                        {employee.type}
                      </span>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* Payroll Calculation Results */}
          <motion.div
            className="bg-white p-6 rounded-xl shadow-lg"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <h2 className="text-xl font-semibold mb-6">Payroll Calculation</h2>
            
            <AnimatePresence mode="wait">
              {payrollData ? (
                <motion.div
                  key="payroll-data"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className="space-y-6"
                >
                  {/* Salary Breakdown */}
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <h3 className="font-semibold mb-3">Salary Breakdown</h3>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div className="flex justify-between">
                        <span>Basic Salary:</span>
                        <span>RM {payrollData.salary_breakdown.basic_salary.toLocaleString()}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Allowances:</span>
                        <span>RM {payrollData.salary_breakdown.allowances.toLocaleString()}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Overtime:</span>
                        <span>RM {payrollData.salary_breakdown.overtime.toLocaleString()}</span>
                      </div>
                      <div className="flex justify-between font-semibold">
                        <span>Gross Salary:</span>
                        <span>RM {payrollData.salary_breakdown.gross_salary.toLocaleString()}</span>
                      </div>
                    </div>
                  </div>

                  {/* Statutory Deductions */}
                  <div className="bg-red-50 p-4 rounded-lg">
                    <h3 className="font-semibold mb-3 text-red-800">Employee Deductions</h3>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span>EPF (11%):</span>
                        <span>RM {payrollData.statutory_deductions.epf.employee}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>SOCSO:</span>
                        <span>RM {payrollData.statutory_deductions.socso.employee}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>EIS (0.2%):</span>
                        <span>RM {payrollData.statutory_deductions.eis.employee}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>PCB (Tax):</span>
                        <span>RM {payrollData.statutory_deductions.pcb}</span>
                      </div>
                    </div>
                  </div>

                  {/* Employer Contributions */}
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <h3 className="font-semibold mb-3 text-blue-800">Employer Contributions</h3>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span>EPF (13%):</span>
                        <span>RM {payrollData.employer_contributions.epf}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>SOCSO:</span>
                        <span>RM {payrollData.employer_contributions.socso}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>EIS (0.2%):</span>
                        <span>RM {payrollData.employer_contributions.eis}</span>
                      </div>
                      <div className="flex justify-between font-semibold">
                        <span>Total:</span>
                        <span>RM {payrollData.employer_contributions.total}</span>
                      </div>
                    </div>
                  </div>

                  {/* Net Salary */}
                  <motion.div
                    className="bg-green-100 p-4 rounded-lg border-2 border-green-300"
                    animate={{ scale: [1, 1.02, 1] }}
                    transition={{ duration: 0.5 }}
                  >
                    <div className="flex justify-between items-center">
                      <span className="text-lg font-semibold text-green-800">Net Salary:</span>
                      <span className="text-2xl font-bold text-green-800">
                        RM {payrollData.salary_breakdown.net_salary.toLocaleString()}
                      </span>
                    </div>
                  </motion.div>

                  {/* Action Buttons */}
                  <div className="flex gap-3">
                    <motion.button
                      className="flex-1 bg-blue-500 text-white py-2 px-4 rounded-lg font-semibold flex items-center justify-center gap-2"
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                    >
                      <Eye size={16} />
                      View Payslip
                    </motion.button>
                    <motion.button
                      className="flex-1 bg-green-500 text-white py-2 px-4 rounded-lg font-semibold flex items-center justify-center gap-2"
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                    >
                      <Download size={16} />
                      Download PDF
                    </motion.button>
                  </div>
                </motion.div>
              ) : (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="text-center text-gray-500 py-12"
                >
                  <Calculator size={48} className="mx-auto mb-4 text-gray-300" />
                  <p>Select an employee to calculate payroll</p>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        </div>

        {/* Monthly Summary */}
        <motion.div
          className="mt-8 bg-white p-6 rounded-xl shadow-lg"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <h2 className="text-xl font-semibold mb-6">Monthly Payroll Summary</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            {[
              { label: 'Total Employees', value: '150', icon: Users, color: 'blue' },
              { label: 'Gross Payroll', value: 'RM 750K', icon: TrendingUp, color: 'green' },
              { label: 'Total Deductions', value: 'RM 125K', icon: Calculator, color: 'red' },
              { label: 'Net Payroll', value: 'RM 625K', icon: FileText, color: 'purple' }
            ].map((stat, index) => (
              <motion.div
                key={stat.label}
                className="text-center"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.4 + index * 0.1 }}
              >
                <div className={`w-16 h-16 mx-auto mb-3 rounded-full bg-${stat.color}-100 flex items-center justify-center`}>
                  <stat.icon className={`text-${stat.color}-600`} size={24} />
                </div>
                <p className="text-2xl font-bold text-gray-800">{stat.value}</p>
                <p className="text-sm text-gray-600">{stat.label}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </motion.div>
    </div>
  );
};

export default PayrollDashboard;