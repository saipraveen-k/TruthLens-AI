import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { FileText, Link2, Upload, ArrowRight, Sparkles } from 'lucide-react';
import TextInput from '../components/Input/TextInput';
import URLInput from '../components/Input/URLInput';
import PDFUpload from '../components/Input/PDFUpload';

const Home = () => {
  const [activeTab, setActiveTab] = useState('text');
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const tabs = [
    { id: 'text', label: 'Paste Text', icon: FileText },
    { id: 'url', label: 'Enter URL', icon: Link2 },
    { id: 'pdf', label: 'Upload PDF', icon: Upload },
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        duration: 0.6,
        staggerChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        type: 'spring',
        stiffness: 100,
      },
    },
  };

  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={containerVariants}
      className="max-w-6xl mx-auto"
    >
      {/* Hero Section */}
      <motion.div variants={itemVariants} className="text-center mb-12">
        <div className="inline-flex items-center space-x-2 bg-white/10 backdrop-blur-sm rounded-full px-4 py-2 mb-6">
          <Sparkles className="w-4 h-4 text-yellow-400" />
          <span className="text-white text-sm font-medium">Powered by Advanced AI</span>
        </div>
        
        <h1 className="text-5xl md:text-7xl font-bold mb-6">
          <span className="gradient-text">TruthLens AI</span>
        </h1>
        
        <p className="text-xl md:text-2xl text-white/90 mb-8 max-w-3xl mx-auto">
          Detect misinformation, analyze bias, and verify credibility with cutting-edge AI technology.
          <span className="block text-lg md:text-xl text-white/80 mt-2">
            Because the truth matters.
          </span>
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
          <div className="flex items-center space-x-2 bg-white/10 backdrop-blur-sm rounded-lg px-4 py-2">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-white text-sm">94% Accuracy</span>
          </div>
          <div className="flex items-center space-x-2 bg-white/10 backdrop-blur-sm rounded-lg px-4 py-2">
            <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
            <span className="text-white text-sm">Real-time Analysis</span>
          </div>
          <div className="flex items-center space-x-2 bg-white/10 backdrop-blur-sm rounded-lg px-4 py-2">
            <div className="w-2 h-2 bg-purple-400 rounded-full"></div>
            <span className="text-white text-sm">Multi-language Support</span>
          </div>
        </div>
      </motion.div>

      {/* Main Input Section */}
      <motion.div variants={itemVariants} className="glass-morphism rounded-3xl p-8">
        {/* Tab Navigation */}
        <div className="flex flex-wrap justify-center mb-8">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center space-x-2 px-6 py-3 rounded-xl font-medium transition-all m-2 ${
                activeTab === tab.id
                  ? 'bg-gradient-to-r from-purple-500 to-blue-500 text-white shadow-lg scale-105'
                  : 'bg-white/10 text-white/80 hover:bg-white/20 hover:text-white'
              }`}
            >
              <tab.icon className="w-5 h-5" />
              <span>{tab.label}</span>
            </button>
          ))}
        </div>

        {/* Input Components */}
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className="min-h-[400px]"
        >
          {activeTab === 'text' && <TextInput isAnalyzing={isAnalyzing} setIsAnalyzing={setIsAnalyzing} />}
          {activeTab === 'url' && <URLInput isAnalyzing={isAnalyzing} setIsAnalyzing={setIsAnalyzing} />}
          {activeTab === 'pdf' && <PDFUpload isAnalyzing={isAnalyzing} setIsAnalyzing={setIsAnalyzing} />}
        </motion.div>
      </motion.div>

      {/* Features Section */}
      <motion.div variants={itemVariants} className="mt-16">
        <h2 className="text-3xl font-bold text-center mb-12 gradient-text">
          Why Choose TruthLens AI?
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            {
              title: 'Advanced AI Analysis',
              description: 'State-of-the-art BERT models analyze text for credibility, bias, and emotional manipulation.',
              icon: '🤖',
            },
            {
              title: 'Explainable Results',
              description: 'Understand why content is flagged with highlighted suspicious sentences and explanations.',
              icon: '🔍',
            },
            {
              title: 'Multi-source Verification',
              description: 'Compare claims against trusted sources and fact-checking databases.',
              icon: '✅',
            },
          ].map((feature, index) => (
            <motion.div
              key={index}
              whileHover={{ scale: 1.05 }}
              className="glass-morphism rounded-2xl p-6 text-center hover-scale"
            >
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-semibold text-white mb-3">{feature.title}</h3>
              <p className="text-white/80">{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* CTA Section */}
      <motion.div variants={itemVariants} className="text-center mt-16">
        <div className="glass-morphism rounded-3xl p-12 bg-gradient-to-r from-purple-600/20 to-blue-600/20">
          <h2 className="text-3xl font-bold gradient-text mb-4">
            Ready to Fight Misinformation?
          </h2>
          <p className="text-xl text-white/90 mb-8 max-w-2xl mx-auto">
            Join thousands of users who are already using TruthLens AI to verify news content 
            and make informed decisions.
          </p>
          <button className="inline-flex items-center space-x-2 bg-gradient-to-r from-purple-500 to-blue-500 text-white px-8 py-4 rounded-xl font-semibold hover:scale-105 transition-all shadow-lg">
            <span>Get Started Now</span>
            <ArrowRight className="w-5 h-5" />
          </button>
        </div>
      </motion.div>
    </motion.div>
  );
};

export default Home;
