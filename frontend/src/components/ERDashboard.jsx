import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Heart, MessageSquare, TrendingUp, AlertCircle } from 'lucide-react';

const ERDashboard = () => {
  const [sentimentData, setSentimentData] = useState(null);

  const analyzeSentiment = async (text) => {
    const response = await fetch('/api/er/sentiment/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    const data = await response.json();
    setSentimentData(data);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 p-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-7xl mx-auto"
      >
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Employee Relations</h1>
          <p className="text-gray-600">Workplace Harmony & Engagement Analytics</p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          {[
            { icon: Heart, label: 'Satisfaction Score', value: '7.2/10', color: 'red' },
            { icon: MessageSquare, label: 'Pulse Surveys', value: '85%', color: 'blue' },
            { icon: TrendingUp, label: 'Engagement', value: '+12%', color: 'green' },
            { icon: AlertCircle, label: 'Burnout Risk', value: '3 High', color: 'orange' }
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

        {/* Sentiment Analysis */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <motion.div
            className="bg-white p-6 rounded-xl shadow-lg"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <h2 className="text-xl font-semibold mb-6">Malaysian Sentiment Analysis</h2>
            <textarea
              className="w-full p-3 border rounded-lg mb-4"
              placeholder="Enter employee feedback in BM/English..."
              rows={4}
              onChange={(e) => analyzeSentiment(e.target.value)}
            />
            {sentimentData && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="space-y-3"
              >
                <div className={`p-3 rounded-lg ${
                  sentimentData.sentiment === 'positive' ? 'bg-green-100' :
                  sentimentData.sentiment === 'negative' ? 'bg-red-100' : 'bg-gray-100'
                }`}>
                  <p className="font-semibold">Sentiment: {sentimentData.sentiment}</p>
                  <p className="text-sm">Score: {sentimentData.sentiment_score}</p>
                  <p className="text-sm">Language: {sentimentData.language}</p>
                </div>
              </motion.div>
            )}
          </motion.div>

          {/* Department Breakdown */}
          <motion.div
            className="bg-white p-6 rounded-xl shadow-lg"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <h2 className="text-xl font-semibold mb-6">Department Satisfaction</h2>
            <div className="space-y-4">
              {[
                { dept: 'IT', score: 8.1, color: 'blue' },
                { dept: 'HR', score: 7.5, color: 'green' },
                { dept: 'Finance', score: 6.8, color: 'yellow' },
                { dept: 'Operations', score: 7.0, color: 'purple' }
              ].map((item, index) => (
                <div key={item.dept} className="flex items-center justify-between">
                  <span className="font-medium">{item.dept}</span>
                  <div className="flex items-center gap-3">
                    <div className="w-32 bg-gray-200 rounded-full h-2">
                      <motion.div
                        className={`bg-${item.color}-500 h-2 rounded-full`}
                        initial={{ width: 0 }}
                        animate={{ width: `${(item.score / 10) * 100}%` }}
                        transition={{ duration: 1, delay: index * 0.2 }}
                      />
                    </div>
                    <span className="font-semibold">{item.score}</span>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </motion.div>
    </div>
  );
};

export default ERDashboard;