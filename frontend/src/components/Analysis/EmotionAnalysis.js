import React from 'react';
import { motion } from 'framer-motion';
import { Heart, Brain, AlertTriangle, Smile } from 'lucide-react';

const EmotionAnalysis = ({ emotionData }) => {
  if (!emotionData) {
    return (
      <div className="glass-morphism rounded-2xl p-6">
        <h3 className="text-lg font-bold text-white mb-4">Emotion Analysis</h3>
        <p className="text-white/60">No emotion data available</p>
      </div>
    );
  }

  const getEmotionColor = (emotion) => {
    const colors = {
      anger: '#ef4444',
      fear: '#f59e0b',
      joy: '#22c55e',
      sadness: '#3b82f6',
      surprise: '#8b5cf6',
      disgust: '#84cc16',
      neutral: '#6b7280'
    };
    return colors[emotion] || '#6b7280';
  };

  const getEmotionIcon = (emotion) => {
    const icons = {
      anger: <AlertTriangle className="w-4 h-4" />,
      fear: <AlertTriangle className="w-4 h-4" />,
      joy: <Smile className="w-4 h-4" />,
      sadness: <Heart className="w-4 h-4" />,
      surprise: <Brain className="w-4 h-4" />,
      disgust: <AlertTriangle className="w-4 h-4" />,
      neutral: <Brain className="w-4 h-4" />
    };
    return icons[emotion] || <Brain className="w-4 h-4" />;
  };

  const emotions = emotionData.emotions?.emotion_scores || {};
  const dominantEmotion = emotionData.emotions?.dominant_emotion || 'neutral';
  const manipulationScore = emotionData.overall_manipulation_score || 0;

  // Sort emotions by score
  const sortedEmotions = Object.entries(emotions)
    .sort(([,a], [,b]) => b - a)
    .slice(0, 5);

  const getManipulationLevel = (score) => {
    if (score >= 0.8) return { label: 'Very High', color: 'text-red-400' };
    if (score >= 0.6) return { label: 'High', color: 'text-orange-400' };
    if (score >= 0.4) return { label: 'Medium', color: 'text-yellow-400' };
    if (score >= 0.2) return { label: 'Low', color: 'text-blue-400' };
    return { label: 'Minimal', color: 'text-green-400' };
  };

  const manipulationLevel = getManipulationLevel(manipulationScore);

  return (
    <motion.div
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.5, delay: 0.5 }}
      className="glass-morphism rounded-2xl p-6"
    >
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-bold text-white">Emotion Analysis</h3>
        <div className="flex items-center space-x-2">
          <Brain className="w-4 h-4 text-white/60" />
          <span className={`text-sm font-medium ${manipulationLevel.color}`}>
            {manipulationLevel.label} Manipulation
          </span>
        </div>
      </div>

      {/* Dominant Emotion */}
      <div className="mb-6 p-4 bg-white/5 rounded-xl">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div 
              className="p-2 rounded-lg"
              style={{ backgroundColor: getEmotionColor(dominantEmotion) + '20' }}
            >
              <div style={{ color: getEmotionColor(dominantEmotion) }}>
                {getEmotionIcon(dominantEmotion)}
              </div>
            </div>
            <div>
              <p className="text-white font-medium capitalize">{dominantEmotion}</p>
              <p className="text-white/60 text-sm">Dominant emotion</p>
            </div>
          </div>
          <div className="text-right">
            <p className="text-2xl font-bold text-white">
              {(emotions[domantEmotion] * 100).toFixed(1)}%
            </p>
            <p className="text-white/60 text-xs">Confidence</p>
          </div>
        </div>
      </div>

      {/* Emotion Bars */}
      <div className="space-y-3 mb-6">
        <h4 className="text-white font-medium mb-3">Emotion Breakdown</h4>
        {sortedEmotions.map(([emotion, score], index) => (
          <motion.div
            key={emotion}
            initial={{ width: 0, opacity: 0 }}
            animate={{ width: '100%', opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.6 + index * 0.1 }}
            className="space-y-1"
          >
            <div className="flex justify-between items-center">
              <div className="flex items-center space-x-2">
                <div 
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: getEmotionColor(emotion) }}
                ></div>
                <span className="text-white/80 text-sm capitalize">{emotion}</span>
              </div>
              <span className="text-white text-sm font-medium">
                {(score * 100).toFixed(1)}%
              </span>
            </div>
            <div className="w-full bg-white/10 rounded-full h-2 overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${score * 100}%` }}
                transition={{ duration: 0.8, delay: 0.7 + index * 0.1 }}
                className="h-full rounded-full"
                style={{ backgroundColor: getEmotionColor(emotion) }}
              />
            </div>
          </motion.div>
        ))}
      </div>

      {/* Analysis Summary */}
      <div className="p-4 bg-white/5 rounded-xl">
        <h4 className="text-white font-medium mb-2">Analysis Summary</h4>
        <div className="space-y-2">
          <div className="flex justify-between items-center">
            <span className="text-white/60 text-sm">Emotional Intensity</span>
            <span className="text-white text-sm font-medium">
              {((emotionData.intensity?.intensity_score || 0) * 100).toFixed(1)}%
            </span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-white/60 text-sm">Emotional Diversity</span>
            <span className="text-white text-sm font-medium">
              {((emotionData.emotions?.emotional_diversity || 0) * 100).toFixed(1)}%
            </span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-white/60 text-sm">Manipulation Score</span>
            <span className={`text-sm font-medium ${manipulationLevel.color}`}>
              {(manipulationScore * 100).toFixed(1)}%
            </span>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default EmotionAnalysis;
