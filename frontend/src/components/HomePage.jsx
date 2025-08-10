import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronRight, Users, Calculator, Shield, Bot, Globe } from 'lucide-react';

const HomePage = () => {
  const [language, setLanguage] = useState('en');
  const [chatVisible, setChatVisible] = useState(false);

  const translations = {
    en: {
      welcome: "AI-Driven HRMS, 100% Malaysia-Compliant",
      subtitle: "Streamline HR operations with Malaysian labor law compliance",
      getStarted: "Get Started",
      watchDemo: "Watch Demo"
    },
    ms: {
      welcome: "HRMS Berkuasa AI, 100% Patuh Malaysia",
      subtitle: "Permudahkan operasi HR dengan pematuhan undang-undang buruh Malaysia",
      getStarted: "Mula Sekarang",
      watchDemo: "Tonton Demo"
    },
    zh: {
      welcome: "AI驱动的人力资源管理系统，100%符合马来西亚法规",
      subtitle: "通过马来西亚劳动法合规简化人力资源运营",
      getStarted: "开始使用",
      watchDemo: "观看演示"
    }
  };

  const features = [
    {
      icon: Calculator,
      title: "Payroll Automation",
      description: "Auto EPF/SOCSO/PCB calculations",
      color: "#FF7900",
      animation: "slideIn"
    },
    {
      icon: Users,
      title: "AI Recruitment",
      description: "Smart candidate matching & bias detection",
      color: "#0066CC",
      animation: "swipe"
    },
    {
      icon: Shield,
      title: "Compliance Tracker",
      description: "Real-time Employment Act updates",
      color: "#00AA44",
      animation: "scroll"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-orange-50">
      {/* Hero Section */}
      <motion.section 
        className="relative px-6 py-20 text-center"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.8 }}
      >
        {/* Language Toggle */}
        <motion.div 
          className="absolute top-4 right-4 flex gap-2"
          initial={{ y: -20 }}
          animate={{ y: 0 }}
        >
          {['en', 'ms', 'zh'].map(lang => (
            <motion.button
              key={lang}
              onClick={() => setLanguage(lang)}
              className={`px-3 py-1 rounded ${language === lang ? 'bg-orange-500 text-white' : 'bg-white'}`}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              {lang.toUpperCase()}
            </motion.button>
          ))}
        </motion.div>

        {/* Animated Welcome Text */}
        <motion.h1 
          className="text-5xl font-bold mb-6 text-gray-800"
          key={language}
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.6 }}
        >
          {translations[language].welcome}
        </motion.h1>

        <motion.p 
          className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto"
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          {translations[language].subtitle}
        </motion.p>

        {/* CTA Buttons */}
        <div className="flex gap-4 justify-center">
          <motion.button
            className="bg-orange-500 text-white px-8 py-3 rounded-lg font-semibold flex items-center gap-2"
            whileHover={{ scale: 1.05, boxShadow: "0 10px 25px rgba(255,121,0,0.3)" }}
            whileTap={{ scale: 0.95 }}
            animate={{ 
              boxShadow: ["0 0 0 0 rgba(255,121,0,0.4)", "0 0 0 10px rgba(255,121,0,0)", "0 0 0 0 rgba(255,121,0,0)"]
            }}
            transition={{ repeat: Infinity, duration: 2 }}
          >
            {translations[language].getStarted}
            <ChevronRight size={20} />
          </motion.button>

          <motion.button
            className="border-2 border-gray-300 text-gray-700 px-8 py-3 rounded-lg font-semibold"
            whileHover={{ scale: 1.05, borderColor: "#FF7900" }}
            whileTap={{ scale: 0.95 }}
          >
            {translations[language].watchDemo}
          </motion.button>
        </div>

        {/* Floating AI Assistant */}
        <motion.div
          className="fixed bottom-6 right-6 z-50"
          animate={{ y: [0, -10, 0] }}
          transition={{ repeat: Infinity, duration: 3 }}
        >
          <motion.button
            onClick={() => setChatVisible(!chatVisible)}
            className="bg-blue-500 text-white p-4 rounded-full shadow-lg"
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
          >
            <Bot size={24} />
          </motion.button>
        </motion.div>
      </motion.section>

      {/* Features Showcase */}
      <section className="px-6 py-16">
        <motion.h2 
          className="text-3xl font-bold text-center mb-12 text-gray-800"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
        >
          Key Features
        </motion.h2>

        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              className="bg-white p-6 rounded-xl shadow-lg cursor-pointer"
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.2 }}
              whileHover={{ 
                scale: 1.05,
                boxShadow: `0 20px 40px ${feature.color}20`
              }}
            >
              <motion.div
                className="w-16 h-16 rounded-full flex items-center justify-center mb-4 mx-auto"
                style={{ backgroundColor: `${feature.color}20` }}
                whileHover={{ rotate: 360 }}
                transition={{ duration: 0.6 }}
              >
                <feature.icon size={32} color={feature.color} />
              </motion.div>
              
              <h3 className="text-xl font-semibold mb-2 text-center">{feature.title}</h3>
              <p className="text-gray-600 text-center">{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Compliance Badges */}
      <section className="px-6 py-16 bg-white">
        <motion.div 
          className="max-w-4xl mx-auto text-center"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
        >
          <h2 className="text-3xl font-bold mb-8 text-gray-800">Malaysia Compliance Ready</h2>
          
          <div className="flex flex-wrap justify-center gap-6">
            {['EPF Ready', 'SOCSO Compliant', 'PDPA 2010', 'Employment Act 1955'].map((badge, index) => (
              <motion.div
                key={badge}
                className="bg-green-100 text-green-800 px-6 py-3 rounded-full font-semibold"
                initial={{ scale: 0 }}
                whileInView={{ scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1, type: "spring" }}
                whileHover={{ scale: 1.1 }}
              >
                ✓ {badge}
              </motion.div>
            ))}
          </div>

          {/* Malaysian Flag Animation */}
          <motion.div
            className="mt-8 flex items-center justify-center gap-2"
            initial={{ x: -100, opacity: 0 }}
            whileInView={{ x: 0, opacity: 1 }}
            viewport={{ once: true }}
          >
            <motion.div
              className="w-8 h-6 bg-gradient-to-r from-red-500 via-white to-blue-500 rounded"
              animate={{ 
                boxShadow: ["0 0 0 0 rgba(255,0,0,0.4)", "0 0 0 10px rgba(255,0,0,0)", "0 0 0 0 rgba(255,0,0,0)"]
              }}
              transition={{ repeat: Infinity, duration: 2 }}
            />
            <span className="text-gray-700 font-semibold">Localized for Malaysia</span>
          </motion.div>
        </motion.div>
      </section>

      {/* AI Chat Demo */}
      <AnimatePresence>
        {chatVisible && (
          <motion.div
            className="fixed bottom-20 right-6 w-80 bg-white rounded-lg shadow-xl z-40"
            initial={{ opacity: 0, y: 20, scale: 0.8 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.8 }}
          >
            <div className="p-4 border-b">
              <h3 className="font-semibold">CikguHR Assistant</h3>
            </div>
            <div className="p-4 h-64 overflow-y-auto">
              <motion.div
                className="bg-gray-100 p-3 rounded-lg mb-3"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.5 }}
              >
                <motion.span
                  initial={{ width: 0 }}
                  animate={{ width: "100%" }}
                  transition={{ duration: 2, delay: 0.5 }}
                  className="block overflow-hidden whitespace-nowrap"
                >
                  CikguHR: How can I help with your HR needs today?
                </motion.span>
              </motion.div>
              
              <motion.div
                className="bg-blue-500 text-white p-3 rounded-lg mb-3 ml-8"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 1.5 }}
              >
                Calculate EPF for RM5000 salary
              </motion.div>

              <motion.div
                className="bg-gray-100 p-3 rounded-lg"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 2.5 }}
              >
                <motion.span
                  initial={{ width: 0 }}
                  animate={{ width: "100%" }}
                  transition={{ duration: 2, delay: 2.5 }}
                  className="block overflow-hidden whitespace-nowrap"
                >
                  Employee: RM550 (11%), Employer: RM650 (13%)
                </motion.span>
              </motion.div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default HomePage;