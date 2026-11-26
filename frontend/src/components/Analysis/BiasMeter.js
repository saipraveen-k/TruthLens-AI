import React from 'react';
import { motion } from 'framer-motion';
import { Scale as Balance, AlertCircle, TrendingUp } from 'lucide-react';

const BiasMeter = ({ biasScore }) => {
  const getBiasData = (score) => {
    if (score >= 0.8) return {
      level: 'Extreme',
      color: 'bg-red-500',
      icon: <AlertCircle className="w-5 h-5" />,
      description: 'Very strong political or ideological bias detected'
    };
    if (score >= 0.6) return {
      level: 'High',
      color: 'bg-orange-500',
      icon: <AlertCircle className="w-5 h-5" />,
      description: 'Strong bias that significantly affects objectivity'
    };
    if (score >= 0.4) return {
      level: 'Medium',
      color: 'bg-yellow-500',
      icon: <Balance className="w-5 h-5" />,
      description: 'Moderate bias that may influence reporting'
    };
    if (score >= 0.2) return {
      level: 'Low',
      color: 'bg-blue-500',
      icon: <TrendingUp className="w-5 h-5" />,
      description: 'Minor bias with minimal impact on objectivity'
    };
    return {
      level: 'Minimal',
      color: 'bg-green-500',
      icon: <Balance className="w-5 h-5" />,
      description: 'Very little bias detected'
    };
  };

  const biasData = getBiasData(parseFloat(biasScore) || 0);
  const biasPercentage = (parseFloat(biasScore) || 0) * 100;

  return (
    <motion.div
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.5, delay: 0.4 }}
      className="glass-morphism rounded-2xl p-6"
    >
      <div className="flex items-center mb-4">
        <div className={`p-2 rounded-lg ${biasData.color.replace('bg-', 'bg-opacity-20 bg-')}`}>
          {biasData.icon}
        </div>
        <div className="ml-3">
          <h3 className="text-lg font-bold text-white">Bias Level</h3>
          <p className="text-white/60 text-sm">Political and ideological bias</p>
        </div>
      </div>

      {/* Bias Meter */}
      <div className="mb-4">
        <div className="flex justify-between items-center mb-2">
          <span className="text-2xl font-bold text-white">{biasPercentage.toFixed(0)}%</span>
          <span className={`px-3 py-1 rounded-full text-xs font-medium ${biasData.color} text-white`}>
            {biasData.level}
          </span>
        </div>
        
        {/* Meter Visual */}
        <div className="relative h-6 bg-gradient-to-r from-green-500 via-yellow-500 via-orange-500 to-red-500 rounded-full overflow-hidden">
          <motion.div
            initial={{ left: '0%' }}
            animate={{ left: `${biasPercentage}%` }}
            transition={{ duration: 1, delay: 0.5, ease: "easeOut" }}
            className="absolute top-1/2 transform -translate-y-1/2 w-1 h-8 bg-white shadow-lg"
            style={{ left: `calc(${biasPercentage}% - 2px)` }}
          >
            <div className="absolute -top-1 left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-b-4 border-l-transparent border-r-transparent border-b-white"></div>
          </motion.div>
        </div>
      </div>

      {/* Scale Labels */}
      <div className="flex justify-between text-xs text-white/60 mb-4">
        <span className="flex items-center">
          <div className="w-2 h-2 bg-green-500 rounded-full mr-1"></div>
          Minimal
        </span>
        <span className="flex items-center">
          <div className="w-2 h-2 bg-yellow-500 rounded-full mr-1"></div>
          Medium
        </span>
        <span className="flex items-center">
          <div className="w-2 h-2 bg-red-500 rounded-full mr-1"></div>
          Extreme
        </span>
      </div>

      {/* Bias Types */}
      <div className="space-y-2 mb-4">
        <div className="flex justify-between items-center p-2 bg-white/5 rounded-lg">
          <span className="text-white/80 text-sm">Political Leaning</span>
          <span className="text-white text-sm font-medium">Center</span>
        </div>
        <div className="flex justify-between items-center p-2 bg-white/5 rounded-lg">
          <span className="text-white/80 text-sm">Subjectivity</span>
          <span className="text-white text-sm font-medium">Moderate</span>
        </div>
        <div className="flex justify-between items-center p-2 bg-white/5 rounded-lg">
          <span className="text-white/80 text-sm">Loaded Language</span>
          <span className="text-white text-sm font-medium">Low</span>
        </div>
      </div>

      {/* Interpretation */}
      <div className="p-3 bg-white/5 rounded-lg">
        <p className="text-white/80 text-sm">
          {biasData.description}. Content with {biasData.level.toLowerCase()} bias should be consumed with awareness of the perspective being presented.
        </p>
      </div>
    </motion.div>
  );
};

export default BiasMeter;
