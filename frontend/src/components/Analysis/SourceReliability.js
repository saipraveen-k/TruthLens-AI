import React from 'react';
import { motion } from 'framer-motion';
import { Globe, CheckCircle, AlertTriangle, XCircle, ExternalLink } from 'lucide-react';

const SourceReliability = ({ sourceInfo }) => {
  if (!sourceInfo) {
    return null;
  }

  const getReliabilityData = (score) => {
    if (!score) {
      return {
        level: 'Unknown',
        color: 'text-gray-400',
        bgColor: 'bg-gray-500/20',
        icon: <AlertTriangle className="w-5 h-5" />,
        description: 'Source reliability could not be determined'
      };
    }
    
    if (score >= 80) return {
      level: 'High',
      color: 'text-green-400',
      bgColor: 'bg-green-500/20',
      icon: <CheckCircle className="w-5 h-5" />,
      description: 'Highly reliable source with strong fact-checking record'
    };
    if (score >= 60) return {
      level: 'Medium',
      color: 'text-yellow-400',
      bgColor: 'bg-yellow-500/20',
      icon: <AlertTriangle className="w-5 h-5" />,
      description: 'Moderately reliable source with some concerns'
    };
    if (score >= 40) return {
      level: 'Low',
      color: 'text-orange-400',
      bgColor: 'bg-orange-500/20',
      icon: <AlertTriangle className="w-5 h-5" />,
      description: 'Low reliability source with credibility issues'
    };
    return {
      level: 'Very Low',
      color: 'text-red-400',
      bgColor: 'bg-red-500/20',
      icon: <XCircle className="w-5 h-5" />,
      description: 'Unreliable source with significant credibility problems'
    };
  };

  const reliabilityData = getReliabilityData(sourceInfo.reliability_score);
  const domain = sourceInfo.domain || 'Unknown';
  const title = sourceInfo.title || 'Unknown Source';

  return (
    <motion.div
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.5, delay: 0.6 }}
      className="glass-morphism rounded-2xl p-6"
    >
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className={`p-2 rounded-lg ${reliabilityData.bgColor}`}>
            {reliabilityData.icon}
          </div>
          <div>
            <h3 className="text-lg font-bold text-white">Source Reliability</h3>
            <p className="text-white/60 text-sm">Domain credibility assessment</p>
          </div>
        </div>
        <div className={`px-3 py-1 rounded-full text-xs font-medium ${reliabilityData.bgColor} ${reliabilityData.color}`}>
          {reliabilityData.level}
        </div>
      </div>

      {/* Source Info */}
      <div className="space-y-4 mb-6">
        <div className="p-4 bg-white/5 rounded-xl">
          <div className="flex items-start justify-between">
            <div className="flex items-center space-x-3">
              <Globe className="w-5 h-5 text-white/60" />
              <div>
                <p className="text-white font-medium">{domain}</p>
                <p className="text-white/60 text-sm">{title}</p>
              </div>
            </div>
            {sourceInfo.url && (
              <a
                href={sourceInfo.url}
                target="_blank"
                rel="noopener noreferrer"
                className="p-2 bg-white/10 hover:bg-white/20 rounded-lg transition-all"
              >
                <ExternalLink className="w-4 h-4 text-white" />
              </a>
            )}
          </div>
        </div>

        {/* Reliability Score */}
        {sourceInfo.reliability_score && (
          <div className="p-4 bg-white/5 rounded-xl">
            <div className="flex justify-between items-center mb-2">
              <span className="text-white/80 text-sm">Reliability Score</span>
              <span className={`text-2xl font-bold ${reliabilityData.color}`}>
                {sourceInfo.reliability_score.toFixed(1)}/100
              </span>
            </div>
            
            {/* Progress Bar */}
            <div className="w-full bg-white/10 rounded-full h-3 overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${sourceInfo.reliability_score}%` }}
                transition={{ duration: 1, delay: 0.7, ease: "easeOut" }}
                className={`h-full rounded-full ${reliabilityData.bgColor.replace('/20', '')}`}
              />
            </div>
          </div>
        )}
      </div>

      {/* Additional Information */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {sourceInfo.author && (
          <div className="p-3 bg-white/5 rounded-lg">
            <p className="text-white/60 text-xs mb-1">Author</p>
            <p className="text-white text-sm font-medium">{sourceInfo.author}</p>
          </div>
        )}
        
        {sourceInfo.publish_date && (
          <div className="p-3 bg-white/5 rounded-lg">
            <p className="text-white/60 text-xs mb-1">Published</p>
            <p className="text-white text-sm font-medium">
              {new Date(sourceInfo.publish_date).toLocaleDateString()}
            </p>
          </div>
        )}
      </div>

      {/* Assessment */}
      <div className="p-4 bg-white/5 rounded-xl">
        <h4 className="text-white font-medium mb-2">Assessment</h4>
        <p className="text-white/80 text-sm mb-3">
          {reliabilityData.description}
        </p>
        
        {/* Source Categories */}
        <div className="flex flex-wrap gap-2">
          {sourceInfo.reliability_score >= 80 && (
            <span className="px-2 py-1 bg-green-500/20 text-green-400 text-xs rounded-full">
              Fact-Checked
            </span>
          )}
          {sourceInfo.reliability_score >= 60 && sourceInfo.reliability_score < 80 && (
            <span className="px-2 py-1 bg-yellow-500/20 text-yellow-400 text-xs rounded-full">
              Mixed Record
            </span>
          )}
          {sourceInfo.reliability_score < 60 && (
            <span className="px-2 py-1 bg-red-500/20 text-red-400 text-xs rounded-full">
              Questionable
            </span>
          )}
          {sourceInfo.category && (
            <span className="px-2 py-1 bg-blue-500/20 text-blue-400 text-xs rounded-full">
              {sourceInfo.category}
            </span>
          )}
        </div>
      </div>

      {/* Notes */}
      {sourceInfo.notes && (
        <div className="p-3 bg-white/5 rounded-lg">
          <p className="text-white/60 text-xs mb-1">Notes</p>
          <p className="text-white/80 text-sm">{sourceInfo.notes}</p>
        </div>
      )}
    </motion.div>
  );
};

export default SourceReliability;
