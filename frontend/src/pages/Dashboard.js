import React from 'react';
import { motion } from 'framer-motion';
import { ArrowLeft, Share2, Download, Clock, Eye, AlertTriangle } from 'lucide-react';
import { useAnalysisStore } from '../stores/authStore';
import CredibilityGauge from '../components/Analysis/CredibilityGauge';
import BiasMeter from '../components/Analysis/BiasMeter';
import FakeProbabilityBar from '../components/Analysis/FakeProbabilityBar';
import EmotionAnalysis from '../components/Analysis/EmotionAnalysis';
import SourceReliability from '../components/Analysis/SourceReliability';
import HighlightedText from '../components/Results/HighlightedText';
import ExplanationCard from '../components/Results/ExplanationCard';

const Dashboard = () => {
  const { currentAnalysis } = useAnalysisStore();

  if (!currentAnalysis) {
    return (
      <div className="text-center py-20">
        <h2 className="text-3xl font-bold text-white mb-4">No Analysis Results</h2>
        <p className="text-white/80 mb-8">
          Please analyze some content first to see results here.
        </p>
        <button
          onClick={() => window.location.href = '/'}
          className="inline-flex items-center space-x-2 bg-gradient-to-r from-purple-500 to-blue-500 text-white px-6 py-3 rounded-xl font-semibold hover:scale-105 transition-all"
        >
          <ArrowLeft className="w-5 h-5" />
          <span>Analyze Content</span>
        </button>
      </div>
    );
  }

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

  const getCredibilityLevel = (score) => {
    if (score >= 80) return { label: 'High', color: 'text-green-400' };
    if (score >= 60) return { label: 'Moderate', color: 'text-yellow-400' };
    if (score >= 40) return { label: 'Low', color: 'text-orange-400' };
    return { label: 'Very Low', color: 'text-red-400' };
  };

  const credibilityLevel = getCredibilityLevel(currentAnalysis.credibility_score);

  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={containerVariants}
      className="max-w-7xl mx-auto"
    >
      {/* Header */}
      <motion.div variants={itemVariants} className="mb-8">
        <div className="glass-morphism rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold gradient-text mb-2">Analysis Results</h1>
              <p className="text-white/80">
                Comprehensive credibility analysis of your content
              </p>
            </div>
            <div className="flex space-x-3">
              <button className="p-2 bg-white/10 hover:bg-white/20 rounded-lg transition-all">
                <Share2 className="w-5 h-5 text-white" />
              </button>
              <button className="p-2 bg-white/10 hover:bg-white/20 rounded-lg transition-all">
                <Download className="w-5 h-5 text-white" />
              </button>
            </div>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-white/5 rounded-xl">
              <p className="text-3xl font-bold text-white mb-1">
                {currentAnalysis.credibility_score.toFixed(1)}%
              </p>
              <p className={`text-sm font-medium ${credibilityLevel.color}`}>
                {credibilityLevel.label} Credibility
              </p>
            </div>
            <div className="text-center p-4 bg-white/5 rounded-xl">
              <p className="text-3xl font-bold text-white mb-1">
                {currentAnalysis.fake_probability.toFixed(1)}%
              </p>
              <p className="text-sm text-red-400 font-medium">Fake Probability</p>
            </div>
            <div className="text-center p-4 bg-white/5 rounded-xl">
              <p className="text-3xl font-bold text-white mb-1">
                {currentAnalysis.bias_score}
              </p>
              <p className="text-sm text-yellow-400 font-medium">Bias Level</p>
            </div>
            <div className="text-center p-4 bg-white/5 rounded-xl">
              <p className="text-3xl font-bold text-white mb-1">
                {currentAnalysis.emotional_manipulation}
              </p>
              <p className="text-sm text-orange-400 font-medium">Emotional Manipulation</p>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Main Analysis Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
        {/* Left Column - Main Metrics */}
        <motion.div variants={itemVariants} className="lg:col-span-2 space-y-6">
          {/* Credibility Gauge */}
          <CredibilityGauge score={currentAnalysis.credibility_score} />
          
          {/* Detailed Analysis */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <FakeProbabilityBar probability={currentAnalysis.fake_probability} />
            <BiasMeter biasScore={currentAnalysis.bias_score} />
          </div>
          
          {/* Emotion Analysis */}
          <EmotionAnalysis emotionData={currentAnalysis.analysis?.emotion} />
          
          {/* Source Reliability */}
          {currentAnalysis.source_info && (
            <SourceReliability sourceInfo={currentAnalysis.source_info} />
          )}
        </motion.div>

        {/* Right Column - Explanations */}
        <motion.div variants={itemVariants} className="space-y-6">
          {/* Risk Factors */}
          <div className="glass-morphism rounded-2xl p-6">
            <h3 className="text-xl font-bold text-white mb-4 flex items-center">
              <AlertTriangle className="w-5 h-5 mr-2 text-yellow-400" />
              Risk Factors
            </h3>
            <div className="space-y-3">
              {currentAnalysis.risk_factors?.map((factor, index) => (
                <div key={index} className="flex items-start space-x-3">
                  <div className="w-2 h-2 bg-yellow-400 rounded-full mt-2"></div>
                  <p className="text-white/80 text-sm">{factor}</p>
                </div>
              ))}
              {(!currentAnalysis.risk_factors || currentAnalysis.risk_factors.length === 0) && (
                <p className="text-green-400 text-sm">No significant risk factors detected</p>
              )}
            </div>
          </div>

          {/* Recommendations */}
          <div className="glass-morphism rounded-2xl p-6">
            <h3 className="text-xl font-bold text-white mb-4">Recommendations</h3>
            <div className="space-y-3">
              {currentAnalysis.recommendations?.map((rec, index) => (
                <div key={index} className="flex items-start space-x-3">
                  <div className="w-2 h-2 bg-blue-400 rounded-full mt-2"></div>
                  <p className="text-white/80 text-sm">{rec}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Analysis Metadata */}
          <div className="glass-morphism rounded-2xl p-6">
            <h3 className="text-xl font-bold text-white mb-4 flex items-center">
              <Eye className="w-5 h-5 mr-2" />
              Analysis Details
            </h3>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-white/60 text-sm">Processing Time</span>
                <span className="text-white text-sm font-medium">
                  {currentAnalysis.metadata?.processing_time || 'N/A'}s
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-white/60 text-sm">Word Count</span>
                <span className="text-white text-sm font-medium">
                  {currentAnalysis.metadata?.word_count?.toLocaleString() || 'N/A'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-white/60 text-sm">Language</span>
                <span className="text-white text-sm font-medium">
                  {currentAnalysis.metadata?.language?.toUpperCase() || 'N/A'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-white/60 text-sm">Analysis ID</span>
                <span className="text-white text-xs font-mono">
                  {currentAnalysis.article_id?.slice(0, 8)}...
                </span>
              </div>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Explainable AI Section */}
      {currentAnalysis.explanation && (
        <motion.div variants={itemVariants} className="space-y-6">
          <div className="glass-morphism rounded-2xl p-6">
            <h3 className="text-2xl font-bold text-white mb-6">Explainable AI Analysis</h3>
            
            {/* Highlighted Text */}
            <HighlightedText 
              explanation={currentAnalysis.explanation} 
              className="mb-6"
            />
            
            {/* Explanation Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <ExplanationCard
                title="Key Factors"
                factors={currentAnalysis.explanation.key_factors}
              />
              <ExplanationCard
                title="Pattern Analysis"
                factors={currentAnalysis.explanation.pattern_analysis}
              />
            </div>
          </div>
        </motion.div>
      )}
    </motion.div>
  );
};

export default Dashboard;
