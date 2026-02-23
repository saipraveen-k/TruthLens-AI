import React from 'react';
import { motion } from 'framer-motion';
import { Clock, Trash2, Eye, Search, Filter } from 'lucide-react';
import { useAnalysisStore } from '../stores/authStore';

const History = () => {
  const { analysisHistory, clearHistory } = useAnalysisStore();

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getCredibilityColor = (score) => {
    if (score >= 80) return 'text-green-400';
    if (score >= 60) return 'text-yellow-400';
    if (score >= 40) return 'text-orange-400';
    return 'text-red-400';
  };

  const getCredibilityLabel = (score) => {
    if (score >= 80) return 'High';
    if (score >= 60) return 'Moderate';
    if (score >= 40) return 'Low';
    return 'Very Low';
  };

  const handleClearHistory = () => {
    if (window.confirm('Are you sure you want to clear all analysis history?')) {
      clearHistory();
    }
  };

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
      {/* Header */}
      <motion.div variants={itemVariants} className="mb-8">
        <div className="glass-morphism rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold gradient-text mb-2">Analysis History</h1>
              <p className="text-white/80">
                Your previous news credibility analyses
              </p>
            </div>
            <div className="flex space-x-3">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-white/60" />
                <input
                  type="text"
                  placeholder="Search history..."
                  className="pl-10 pr-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                />
              </div>
              <button className="p-2 bg-white/10 hover:bg-white/20 rounded-lg transition-all">
                <Filter className="w-4 h-4 text-white" />
              </button>
              {analysisHistory.length > 0 && (
                <button
                  onClick={handleClearHistory}
                  className="p-2 bg-red-500/20 hover:bg-red-500/30 rounded-lg transition-all"
                >
                  <Trash2 className="w-4 h-4 text-red-400" />
                </button>
              )}
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-white/5 rounded-xl">
              <p className="text-2xl font-bold text-white mb-1">
                {analysisHistory.length}
              </p>
              <p className="text-white/60 text-sm">Total Analyses</p>
            </div>
            <div className="text-center p-4 bg-white/5 rounded-xl">
              <p className="text-2xl font-bold text-green-400 mb-1">
                {analysisHistory.filter(a => a.credibility_score >= 80).length}
              </p>
              <p className="text-white/60 text-sm">High Credibility</p>
            </div>
            <div className="text-center p-4 bg-white/5 rounded-xl">
              <p className="text-2xl font-bold text-red-400 mb-1">
                {analysisHistory.filter(a => a.fake_probability >= 80).length}
              </p>
              <p className="text-white/60 text-sm">Likely Fake</p>
            </div>
            <div className="text-center p-4 bg-white/5 rounded-xl">
              <p className="text-2xl font-bold text-white mb-1">
                {analysisHistory.length > 0 
                  ? (analysisHistory.reduce((sum, a) => sum + a.credibility_score, 0) / analysisHistory.length).toFixed(1)
                  : '0'
                }%
              </p>
              <p className="text-white/60 text-sm">Avg Credibility</p>
            </div>
          </div>
        </div>
      </motion.div>

      {/* History List */}
      <motion.div variants={itemVariants} className="space-y-4">
        {analysisHistory.length === 0 ? (
          <div className="glass-morphism rounded-2xl p-12 text-center">
            <Clock className="w-16 h-16 text-white/60 mx-auto mb-4" />
            <h3 className="text-xl font-bold text-white mb-2">No Analysis History</h3>
            <p className="text-white/80 mb-6">
              You haven't analyzed any content yet. Start by analyzing some news articles or text.
            </p>
            <button
              onClick={() => window.location.href = '/'}
              className="inline-flex items-center space-x-2 bg-gradient-to-r from-purple-500 to-blue-500 text-white px-6 py-3 rounded-xl font-semibold hover:scale-105 transition-all"
            >
              <span>Analyze Content</span>
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            {analysisHistory.map((analysis, index) => (
              <motion.div
                key={analysis.article_id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: 0.1 + index * 0.05 }}
                className="glass-morphism rounded-2xl p-6 hover:scale-[1.02] transition-all cursor-pointer"
                onClick={() => {
                  // Set current analysis and navigate to dashboard
                  const { setAnalysis } = useAnalysisStore.getState();
                  setAnalysis(analysis);
                  window.location.href = '/dashboard';
                }}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <h3 className="text-lg font-semibold text-white">
                        {analysis.title || 'Untitled Analysis'}
                      </h3>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getCredibilityColor(analysis.credibility_score)}`}>
                        {getCredibilityLabel(analysis.credibility_score)}
                      </span>
                    </div>
                    
                    {analysis.url && (
                      <p className="text-white/60 text-sm mb-2 truncate">
                        {analysis.url}
                      </p>
                    )}

                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-3">
                      <div>
                        <p className="text-white/60 text-xs">Credibility</p>
                        <p className={`text-lg font-bold ${getCredibilityColor(analysis.credibility_score)}`}>
                          {analysis.credibility_score.toFixed(1)}%
                        </p>
                      </div>
                      <div>
                        <p className="text-white/60 text-xs">Fake Prob.</p>
                        <p className="text-lg font-bold text-red-400">
                          {analysis.fake_probability.toFixed(1)}%
                        </p>
                      </div>
                      <div>
                        <p className="text-white/60 text-xs">Bias</p>
                        <p className="text-lg font-bold text-yellow-400">
                          {analysis.bias_score}
                        </p>
                      </div>
                      <div>
                        <p className="text-white/60 text-xs">Words</p>
                        <p className="text-lg font-bold text-white">
                          {analysis.metadata?.word_count?.toLocaleString() || 'N/A'}
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="flex flex-col items-end space-y-2 ml-4">
                    <span className="text-white/60 text-sm">
                      {formatDate(analysis.created_at)}
                    </span>
                    <button className="p-2 bg-white/10 hover:bg-white/20 rounded-lg transition-all">
                      <Eye className="w-4 h-4 text-white" />
                    </button>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </motion.div>
    </motion.div>
  );
};

export default History;
