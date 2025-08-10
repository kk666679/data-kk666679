import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { BookOpen, Award, Clock, TrendingUp } from 'lucide-react';

const LDDashboard = () => {
  const [selectedCourse, setSelectedCourse] = useState(null);

  const courses = [
    { id: 1, title: 'Workplace Safety (BM)', duration: 15, language: 'BM', hrdf: true, progress: 75 },
    { id: 2, title: 'Digital Marketing Basics', duration: 20, language: 'EN', hrdf: true, progress: 45 },
    { id: 3, title: 'Team Leadership Skills', duration: 25, language: 'EN', hrdf: true, progress: 90 },
    { id: 4, title: 'Malaysian Labor Laws', duration: 30, language: 'BM', hrdf: true, progress: 60 }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-indigo-50 p-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-7xl mx-auto"
      >
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Learning & Development</h1>
          <p className="text-gray-600">HRDF-Claimable Training & Skill Development</p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          {[
            { icon: BookOpen, label: 'Active Courses', value: '45', color: 'blue' },
            { icon: Award, label: 'Certifications', value: '128', color: 'green' },
            { icon: Clock, label: 'Training Hours', value: '2,340', color: 'purple' },
            { icon: TrendingUp, label: 'Completion Rate', value: '78%', color: 'orange' }
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

        {/* Course Library */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <motion.div
            className="bg-white p-6 rounded-xl shadow-lg"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <h2 className="text-xl font-semibold mb-6">Course Library</h2>
            <div className="space-y-4">
              {courses.map((course, index) => (
                <motion.div
                  key={course.id}
                  className="border rounded-lg p-4 cursor-pointer hover:shadow-md transition-shadow"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  whileHover={{ scale: 1.02 }}
                  onClick={() => setSelectedCourse(course)}
                >
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <h3 className="font-semibold">{course.title}</h3>
                      <p className="text-sm text-gray-600">{course.duration} minutes • {course.language}</p>
                    </div>
                    {course.hrdf && (
                      <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded">
                        HRDF
                      </span>
                    )}
                  </div>
                  
                  <div className="mb-2">
                    <div className="flex justify-between text-sm mb-1">
                      <span>Progress</span>
                      <span>{course.progress}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <motion.div
                        className="bg-purple-500 h-2 rounded-full"
                        initial={{ width: 0 }}
                        animate={{ width: `${course.progress}%` }}
                        transition={{ duration: 1, delay: index * 0.2 }}
                      />
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* HRDF Claim Status */}
          <motion.div
            className="bg-white p-6 rounded-xl shadow-lg"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <h2 className="text-xl font-semibold mb-6">HRDF Claim Status</h2>
            
            <div className="space-y-4">
              {[
                { id: 'HRDF-001', status: 'approved', amount: 2500, course: 'Leadership Training' },
                { id: 'HRDF-002', status: 'pending', amount: 1800, course: 'Digital Skills' },
                { id: 'HRDF-003', status: 'under_review', amount: 3200, course: 'Safety Certification' }
              ].map((claim, index) => (
                <motion.div
                  key={claim.id}
                  className="border rounded-lg p-4"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <h3 className="font-semibold">{claim.id}</h3>
                      <p className="text-sm text-gray-600">{claim.course}</p>
                    </div>
                    <span className={`px-2 py-1 rounded text-xs ${
                      claim.status === 'approved' ? 'bg-green-100 text-green-800' :
                      claim.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-blue-100 text-blue-800'
                    }`}>
                      {claim.status.replace('_', ' ')}
                    </span>
                  </div>
                  <p className="text-lg font-semibold text-purple-600">
                    RM {claim.amount.toLocaleString()}
                  </p>
                </motion.div>
              ))}
            </div>

            <motion.div
              className="mt-6 p-4 bg-purple-50 rounded-lg"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
            >
              <h3 className="font-semibold text-purple-800 mb-2">Total Claimable</h3>
              <p className="text-2xl font-bold text-purple-600">RM 7,500</p>
              <p className="text-sm text-purple-600">Available this year</p>
            </motion.div>
          </motion.div>
        </div>
      </motion.div>
    </div>
  );
};

export default LDDashboard;