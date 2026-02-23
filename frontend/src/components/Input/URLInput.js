import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Link, Send, Globe, Sparkles } from 'lucide-react';
import { useAnalysisStore } from '../../stores/authStore';
import { analysisAPI } from '../../services/api';
import toast from 'react-hot-toast';

const URLInput = ({ isAnalyzing, setIsAnalyzing }) => {
  const [url, setUrl] = useState('');
  const [extractFullText, setExtractFullText] = useState(true);
  const { setAnalysis, addToHistory } = useAnalysisStore();

  const validateURL = (url) => {
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!url.trim()) {
      toast.error('Please enter a URL to analyze');
      return;
    }

    // Add protocol if missing
    let processedUrl = url.trim();
    if (!processedUrl.startsWith('http://') && !processedUrl.startsWith('https://')) {
      processedUrl = 'https://' + processedUrl;
    }

    if (!validateURL(processedUrl)) {
      toast.error('Please enter a valid URL');
      return;
    }

    setIsAnalyzing(true);
    
    try {
      const result = await analysisAPI.analyzeURL({ 
        url: processedUrl, 
        extract_full_text: extractFullText 
      });
      
      setAnalysis(result);
      addToHistory(result);
      
      toast.success('Article analyzed successfully!');
      
      // Redirect to results
      window.location.href = '/dashboard';
      
    } catch (error) {
      console.error('Analysis error:', error);
      toast.error(error.response?.data?.detail || 'Failed to analyze URL. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleClear = () => {
    setUrl('');
  };

  const popularSources = [
    { name: 'BBC News', url: 'https://www.bbc.com/news' },
    { name: 'CNN', url: 'https://www.cnn.com' },
    { name: 'Reuters', url: 'https://www.reuters.com' },
    { name: 'The Guardian', url: 'https://www.theguardian.com' },
  ];

  return (
    <div className="h-full flex flex-col">
      <form onSubmit={handleSubmit} className="flex-1 flex flex-col">
        <div className="mb-6">
          <h3 className="text-2xl font-bold text-white mb-2">Analyze Article URL</h3>
          <p className="text-white/80">
            Enter the URL of a news article or web content you want to verify.
          </p>
        </div>

        <div className="flex-1 space-y-4">
          {/* URL Input */}
          <div className="relative">
            <div className="absolute left-4 top-1/2 transform -translate-y-1/2">
              <Globe className="w-5 h-5 text-white/60" />
            </div>
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://example.com/news-article"
              className="w-full pl-12 pr-4 py-4 bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
              disabled={isAnalyzing}
            />
          </div>

          {/* Options */}
          <div className="flex items-center space-x-3 p-4 bg-white/5 rounded-xl">
            <input
              type="checkbox"
              id="extractFullText"
              checked={extractFullText}
              onChange={(e) => setExtractFullText(e.target.checked)}
              className="w-4 h-4 text-purple-500 bg-white/10 border-white/20 rounded focus:ring-purple-500 focus:ring-2"
              disabled={isAnalyzing}
            />
            <label htmlFor="extractFullText" className="text-white/80 text-sm cursor-pointer">
              Extract full article content (recommended for better analysis)
            </label>
          </div>

          {/* Popular Sources */}
          <div className="p-4 bg-white/5 rounded-xl">
            <h4 className="text-white font-semibold mb-3 text-sm">Popular Sources for Testing:</h4>
            <div className="grid grid-cols-2 gap-2">
              {popularSources.map((source, index) => (
                <button
                  key={index}
                  type="button"
                  onClick={() => setUrl(source.url)}
                  className="text-left p-2 bg-white/10 hover:bg-white/20 rounded-lg text-white/80 hover:text-white text-sm transition-all"
                >
                  {source.name}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center justify-between mt-6">
          <div className="flex items-center space-x-4">
            <button
              type="button"
              onClick={handleClear}
              disabled={isAnalyzing || !url}
              className="px-6 py-3 bg-white/10 text-white rounded-xl hover:bg-white/20 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              Clear
            </button>
            
            <div className="flex items-center space-x-2 text-white/60 text-sm">
              <Link className="w-4 h-4" />
              <span>Supports most news websites</span>
            </div>
          </div>

          <button
            type="submit"
            disabled={isAnalyzing || !url.trim()}
            className="flex items-center space-x-2 bg-gradient-to-r from-purple-500 to-blue-500 text-white px-8 py-3 rounded-xl font-semibold hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:scale-100 transition-all shadow-lg"
          >
            {isAnalyzing ? (
              <>
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5" />
                <span>Analyze URL</span>
              </>
            )}
          </button>
        </div>
      </form>

      {/* Tips */}
      <div className="mt-6 p-4 bg-green-500/20 border border-green-400/30 rounded-xl">
        <h4 className="text-white font-semibold mb-2 flex items-center">
          <Sparkles className="w-4 h-4 mr-2" />
          URL Analysis Tips
        </h4>
        <ul className="text-white/80 text-sm space-y-1">
          <li>• Works with most news websites and blogs</li>
          <li>• Full text extraction provides better analysis accuracy</li>
          <li>• Some paywalled content may not be accessible</li>
          <li>• Analysis includes source reliability assessment</li>
        </ul>
      </div>
    </div>
  );
};

export default URLInput;
