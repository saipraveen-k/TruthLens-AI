import React from 'react';
import { motion } from 'framer-motion';
import { AlertTriangle, Balance, TrendingUp } from 'lucide-react';

const FakeProbabilityBar = ({ probability }) => {
  const getProbabilityColor = (prob) => {
    if (prob >= 80) return 'bg-red-500';
    if (prob >= 60) return 'bg-orange-500';
    if (prob >= 40) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  const getProbabilityLabel = (prob) => {
    if (prob >= 80) return 'Very High';
    if (prob >= 60) return 'High';
    if (prob >= 40) return 'Moderate';
    return 'Low';
  };

  const getProbabilityIcon = (prob) => {
    if (prob >= 60) return <AlertTriangle className="w-5 h-5" />;
    return <TrendingUp className="w-5 h-5" />;
  };

  const barColor = getProbabilityColor(probability);
  const probabilityLabel = getProbabilityLabel(probability);
  const probabilityIcon = getProbabilityIcon(probability);

  return (
    <motion.div
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.5, delay: 0.3 }}
      className="glass-morphism rounded-2xl p-6"
    >
      <div className="flex items-center mb-4">
        <div className={`p-2 rounded-lg ${probabilityColor.replace('bg-', 'bg-opacity-20 bg-')}`}>
          {probabilityIcon}
        </div>
        <div className="ml-3">
          <h3 className="text-lg font-bold text-white">Fake Probability</h3>
          <p className="text-white/60 text-sm">Likelihood of misinformation</p>
        </div>
      </div>

      {/* Probability Bar */}
      <div className="mb-4">
        <div className="flex justify-between items-center mb-2">
          <span className="text-2xl font-bold text-white">{probability.toFixed(1)}%</span>
          <span className={`px-3 py-1 rounded-full text-xs font-medium ${barColor} text-white`}>
            {probabilityLabel}
          </span>
        </div>
        
        {/* Progress Bar */}
        <div className="w-full bg-white/10 rounded-full h-4 overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${probability}%` }}
            transition={{ duration: 1, delay: 0.5, ease: "easeOut" }}
            className={`h-full ${barColor} relative overflow-hidden`}
          >
            {/* Animated shine effect */}
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-pulse"></div>
          </motion.div>
        </div>
      </div>

      {/* Scale */}
      <div className="flex justify-between text-xs text-white/60 mb-4">
        <span>0%</span>
        <span>25%</span>
        <span>50%</span>
        <span>75%</span>
        <span>100%</span>
      </div>

      {/* Interpretation */}
      <div className="p-3 bg-white/5 rounded-lg">
        <p className="text-white/80 text-sm">
          {probability >= 80 && "This content is very likely to be fake news. Do not share."}
          {probability >= 60 && probability < 80 && "This content shows strong signs of being fake. Verify with trusted sources."}
          {probability >= 40 && probability < 60 && "This content has some fake characteristics. Be cautious."}
          {probability < 40 && "This content appears to be real news."}
        </p>
      </div>
    </motion.div>
  );
};

export default FakeProbabilityBar;
