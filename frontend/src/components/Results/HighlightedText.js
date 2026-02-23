import React from 'react';
import { motion } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const HighlightedText = ({ explanation, className = '' }) => {
  if (!explanation || !explanation.highlighted_text) {
    return (
      <div className={`glass-morphism rounded-2xl p-6 ${className}`}>
        <h3 className="text-lg font-bold text-white mb-4">Highlighted Analysis</h3>
        <p className="text-white/60">No highlighted text available</p>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.7 }}
      className={`glass-morphism rounded-2xl p-6 ${className}`}
    >
      <div className="mb-6">
        <h3 className="text-lg font-bold text-white mb-2">Explainable AI Analysis</h3>
        <p className="text-white/60 text-sm">
          Suspicious content has been highlighted with explanations
        </p>
      </div>

      {/* Highlighted Text */}
      <div className="mb-6">
        <div className="p-6 bg-white/5 rounded-xl leading-relaxed">
          <div 
            className="text-white/90 text-sm"
            dangerouslySetInnerHTML={{ __html: explanation.highlighted_text }}
          />
        </div>
      </div>

      {/* Legend */}
      <div className="mb-6">
        <h4 className="text-white font-medium mb-3">Highlight Legend</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div className="flex items-center space-x-3">
            <div className="w-4 h-4 bg-red-500/20 border-b-2 border-red-500 rounded"></div>
            <span className="text-white/80 text-sm">Highly Suspicious</span>
          </div>
          <div className="flex items-center space-x-3">
            <div className="w-4 h-4 bg-orange-500/20 border-b-2 border-orange-500 rounded"></div>
            <span className="text-white/80 text-sm">Moderately Suspicious</span>
          </div>
          <div className="flex items-center space-x-3">
            <div className="w-4 h-4 bg-yellow-500/20 border-b-2 border-yellow-500 rounded"></div>
            <span className="text-white/80 text-sm">Low Suspicious</span>
          </div>
          <div className="flex items-center space-x-3">
            <div className="w-4 h-4 bg-blue-500/20 border-b-2 border-blue-500 rounded"></div>
            <span className="text-white/80 text-sm">Pattern Detected</span>
          </div>
        </div>
      </div>

      {/* Key Factors */}
      {explanation.key_factors && explanation.key_factors.length > 0 && (
        <div className="mb-6">
          <h4 className="text-white font-medium mb-3">Key Factors</h4>
          <div className="space-y-2">
            {explanation.key_factors.map((factor, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: 0.8 + index * 0.1 }}
                className="p-3 bg-white/5 rounded-lg border-l-4 border-red-500"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <p className="text-white/80 text-sm mb-1">
                      <span className="font-medium text-white">"{factor.text}"</span>
                    </p>
                    <p className="text-white/60 text-xs">{factor.reason}</p>
                  </div>
                  <div className="ml-3 text-right">
                    <span className={`text-xs font-medium px-2 py-1 rounded ${
                      factor.impact < -0.3 ? 'bg-red-500/20 text-red-400' :
                      factor.impact < -0.1 ? 'bg-orange-500/20 text-orange-400' :
                      'bg-yellow-500/20 text-yellow-400'
                    }`}>
                      {factor.impact < -0.3 ? 'High Impact' :
                       factor.impact < -0.1 ? 'Medium Impact' : 'Low Impact'}
                    </span>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {/* Summary Statistics */}
      {explanation.explanation_summary && (
        <div className="p-4 bg-white/5 rounded-xl">
          <h4 className="text-white font-medium mb-3">Analysis Summary</h4>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <p className="text-2xl font-bold text-white mb-1">
                {explanation.explanation_summary.total_sentences || 0}
              </p>
              <p className="text-white/60 text-xs">Total Sentences</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-red-400 mb-1">
                {explanation.explanation_summary.suspicious_sentences || 0}
              </p>
              <p className="text-white/60 text-xs">Suspicious</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-yellow-400 mb-1">
                {explanation.explanation_summary.suspicious_percentage || 0}%
              </p>
              <p className="text-white/60 text-xs">Suspicious %</p>
            </div>
            <div className="text-center">
              <p className="text-lg font-bold text-blue-400 mb-1">
                {explanation.explanation_summary.most_common_pattern || 'None'}
              </p>
              <p className="text-white/60 text-xs">Common Pattern</p>
            </div>
          </div>
        </div>
      )}

      {/* Instructions */}
      <div className="p-4 bg-blue-500/20 border border-blue-400/30 rounded-xl">
        <h4 className="text-white font-semibold mb-2">How to Use This Analysis</h4>
        <ul className="text-white/80 text-sm space-y-1">
          <li>• Hover over highlighted text to see detailed explanations</li>
          <li>• Pay special attention to red and orange highlights</li>
          <li>• Consider the context and source of the information</li>
          <li>• Verify claims with multiple reliable sources</li>
        </ul>
      </div>
    </motion.div>
  );
};

export default HighlightedText;
