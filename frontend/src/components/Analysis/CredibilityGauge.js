import React from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, AlertTriangle, CheckCircle, Clock } from 'lucide-react';

const CredibilityGauge = ({ score }) => {
  const getGaugeColor = (score) => {
    if (score >= 80) return '#22c55e';  // green
    if (score >= 60) return '#f59e0b';  // yellow
    if (score >= 40) return '#fb923c';  // orange
    return '#ef4444';  // red
  };

  const getGaugeLabel = (score) => {
    if (score >= 80) return 'Highly Credible';
    if (score >= 60) return 'Moderately Credible';
    if (score >= 40) return 'Low Credibility';
    return 'Very Low Credibility';
  };

  const getGaugeIcon = (score) => {
    if (score >= 80) return <CheckCircle className="w-6 h-6" />;
    if (score >= 60) return <TrendingUp className="w-6 h-6" />;
    return <AlertTriangle className="w-6 h-6" />;
  };

  const gaugeColor = getGaugeColor(score);
  const gaugeLabel = getGaugeLabel(score);
  const gaugeIcon = getGaugeIcon(score);

  // Calculate rotation for the gauge needle
  const rotation = (score / 100) * 180 - 90; // -90 to 90 degrees

  return (
    <motion.div
      initial={{ scale: 0.8, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.5, delay: 0.2 }}
      className="glass-morphism rounded-2xl p-6"
    >
      <div className="flex flex-col items-center">
        <h3 className="text-xl font-bold text-white mb-6">Credibility Score</h3>
        
        {/* SVG Gauge */}
        <div className="relative w-64 h-32 mb-6">
          <svg
            width="256"
            height="128"
            viewBox="0 0 256 128"
            className="transform -rotate-90"
          >
            {/* Background arc */}
            <path
              d="M 16 112 A 96 96 0 0 1 240 112"
              fill="none"
              stroke="rgba(255, 255, 255, 0.1)"
              strokeWidth="16"
              strokeLinecap="round"
            />
            
            {/* Colored arc segments */}
            <path
              d="M 16 112 A 96 96 0 0 1 80 32"
              fill="none"
              stroke="#ef4444"
              strokeWidth="16"
              strokeLinecap="round"
              opacity="0.8"
            />
            <path
              d="M 80 32 A 96 96 0 0 1 144 32"
              fill="none"
              stroke="#fb923c"
              strokeWidth="16"
              strokeLinecap="round"
              opacity="0.8"
            />
            <path
              d="M 144 32 A 96 96 0 0 1 208 32"
              fill="none"
              stroke="#f59e0b"
              strokeWidth="16"
              strokeLinecap="round"
              opacity="0.8"
            />
            <path
              d="M 208 32 A 96 96 0 0 1 240 112"
              fill="none"
              stroke="#22c55e"
              strokeWidth="16"
              strokeLinecap="round"
              opacity="0.8"
            />
            
            {/* Needle */}
            <g transform={`translate(128, 112) rotate(${rotation})`}>
              <line
                x1="0"
                y1="0"
                x2="0"
                y2="-80"
                stroke="#ffffff"
                strokeWidth="4"
                strokeLinecap="round"
                className="drop-shadow-lg"
              />
              <circle cx="0" cy="0" r="8" fill="#ffffff" />
            </g>
          </svg>
          
          {/* Center text */}
          <div className="absolute inset-0 flex flex-col items-center justify-center mt-8">
            <div className="text-4xl font-bold text-white mb-1">
              {score.toFixed(1)}%
            </div>
            <div 
              className="text-sm font-medium flex items-center"
              style={{ color: gaugeColor }}
            >
              {gaugeIcon}
              <span className="ml-2">{gaugeLabel}</span>
            </div>
          </div>
        </div>

        {/* Scale labels */}
        <div className="flex justify-between w-full max-w-xs mb-4">
          <div className="text-center">
            <div className="w-3 h-3 bg-red-500 rounded-full mb-1"></div>
            <span className="text-xs text-white/60">0%</span>
          </div>
          <div className="text-center">
            <div className="w-3 h-3 bg-orange-500 rounded-full mb-1"></div>
            <span className="text-xs text-white/60">25%</span>
          </div>
          <div className="text-center">
            <div className="w-3 h-3 bg-yellow-500 rounded-full mb-1"></div>
            <span className="text-xs text-white/60">50%</span>
          </div>
          <div className="text-center">
            <div className="w-3 h-3 bg-yellow-500 rounded-full mb-1"></div>
            <span className="text-xs text-white/60">75%</span>
          </div>
          <div className="text-center">
            <div className="w-3 h-3 bg-green-500 rounded-full mb-1"></div>
            <span className="text-xs text-white/60">100%</span>
          </div>
        </div>

        {/* Interpretation */}
        <div className="text-center p-4 bg-white/5 rounded-xl max-w-sm">
          <p className="text-white/80 text-sm">
            {score >= 80 && "This content appears highly credible and trustworthy."}
            {score >= 60 && score < 80 && "This content appears moderately credible but verify important claims."}
            {score >= 40 && score < 60 && "This content shows some credibility concerns. Exercise caution."}
            {score < 40 && "This content appears unreliable. Seek trusted sources."}
          </p>
        </div>
      </div>
    </motion.div>
  );
};

export default CredibilityGauge;
