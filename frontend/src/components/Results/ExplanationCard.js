import React from 'react';
import { motion } from 'framer-motion';
import { AlertTriangle, Info, CheckCircle, XCircle } from 'lucide-react';

const ExplanationCard = ({ title, factors = [] }) => {
  const getFactorIcon = (type) => {
    const icons = {
      'unsubstantiated_claims': <XCircle className="w-4 h-4" />,
      'emotional_manipulation': <AlertTriangle className="w-4 h-4" />,
      'clickbait_patterns': <Info className="w-4 h-4" />,
      'authority_appeals': <CheckCircle className="w-4 h-4" />,
      'conspiracy_indicators': <AlertTriangle className="w-4 h-4" />
    };
    return icons[type] || <Info className="w-4 h-4" />;
  };

  const getFactorColor = (type) => {
    const colors = {
      'unsubstantiated_claims': 'border-red-500 bg-red-500/10',
      'emotional_manipulation': 'border-orange-500 bg-orange-500/10',
      'clickbait_patterns': 'border-yellow-500 bg-yellow-500/10',
      'authority_appeals': 'border-blue-500 bg-blue-500/10',
      'conspiracy_indicators': 'border-purple-500 bg-purple-500/10'
    };
    return colors[type] || 'border-gray-500 bg-gray-500/10';
  };

  if (!factors || factors.length === 0) {
    return (
      <div className="glass-morphism rounded-2xl p-6">
        <h3 className="text-lg font-bold text-white mb-4">{title}</h3>
        <p className="text-white/60">No factors to display</p>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.8 }}
      className="glass-morphism rounded-2xl p-6"
    >
      <h3 className="text-lg font-bold text-white mb-4">{title}</h3>
      
      <div className="space-y-3">
        {factors.map((factor, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3, delay: 0.9 + index * 0.1 }}
            className={`p-4 rounded-xl border-l-4 ${getFactorColor(factor.type || 'default')}`}
          >
            <div className="flex items-start space-x-3">
              <div className="mt-1">
                {getFactorIcon(factor.type)}
              </div>
              <div className="flex-1">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="text-white font-medium capitalize">
                    {factor.type?.replace('_', ' ') || 'Unknown Pattern'}
                  </h4>
                  {factor.impact && (
                    <span className={`text-xs px-2 py-1 rounded-full ${
                      factor.impact < -0.3 ? 'bg-red-500/20 text-red-400' :
                      factor.impact < -0.1 ? 'bg-orange-500/20 text-orange-400' :
                      'bg-yellow-500/20 text-yellow-400'
                    }`}>
                      {factor.impact < -0.3 ? 'High' :
                       factor.impact < -0.1 ? 'Medium' : 'Low'} Impact
                    </span>
                  )}
                </div>
                
                {factor.text && (
                  <div className="mb-3">
                    <p className="text-white/80 text-sm mb-1">
                      <span className="font-medium">Detected Text:</span> "{factor.text}"
                    </p>
                  </div>
                )}
                
                {factor.explanation && (
                  <div className="mb-3">
                    <p className="text-white/70 text-sm">
                      <span className="font-medium">Explanation:</span> {factor.explanation}
                    </p>
                  </div>
                )}

                {factor.matches && factor.matches.length > 0 && (
                  <div>
                    <p className="text-white/60 text-xs mb-1">
                      <span className="font-medium">Matches:</span>
                    </p>
                    <div className="flex flex-wrap gap-1">
                      {factor.matches.map((match, matchIndex) => (
                        <span
                          key={matchIndex}
                          className="px-2 py-1 bg-white/10 rounded text-xs text-white/80"
                        >
                          {match}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {factor.reason && (
                  <div>
                    <p className="text-white/70 text-sm">
                      <span className="font-medium">Reason:</span> {factor.reason}
                    </p>
                  </div>
                )}

                {factor.confidence && (
                  <div className="mt-2 pt-2 border-t border-white/10">
                    <div className="flex justify-between items-center">
                      <span className="text-white/60 text-xs">Confidence</span>
                      <span className="text-white text-sm font-medium">
                        {(factor.confidence * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Summary */}
      <div className="mt-4 p-3 bg-white/5 rounded-lg">
        <p className="text-white/80 text-sm">
          <span className="font-medium">Summary:</span> {factors.length} {title.toLowerCase()} detected in this content.
          {factors.some(f => f.impact < -0.3) && ' Some factors show high impact on credibility.'}
        </p>
      </div>
    </motion.div>
  );
};

export default ExplanationCard;
