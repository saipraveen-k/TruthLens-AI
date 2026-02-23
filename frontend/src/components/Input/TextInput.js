import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Send, FileText, Sparkles } from 'lucide-react';
import { useAnalysisStore } from '../../stores/authStore';
import { analysisAPI } from '../../services/api';
import toast from 'react-hot-toast';

const TextInput = ({ isAnalyzing, setIsAnalyzing }) => {
  const [text, setText] = useState('');
  const { setAnalysis, addToHistory } = useAnalysisStore();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!text.trim()) {
      toast.error('Please enter some text to analyze');
      return;
    }

    if (text.length < 50) {
      toast.error('Text must be at least 50 characters long');
      return;
    }

    if (text.length > 10000) {
      toast.error('Text must be less than 10,000 characters');
      return;
    }

    setIsAnalyzing(true);
    
    try {
      const result = await analysisAPI.analyzeText({ text });
      
      setAnalysis(result);
      addToHistory(result);
      
      toast.success('Analysis completed successfully!');
      
      // Redirect to results
      window.location.href = '/dashboard';
      
    } catch (error) {
      console.error('Analysis error:', error);
      toast.error(error.response?.data?.detail || 'Analysis failed. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleClear = () => {
    setText('');
  };

  const charCount = text.length;
  const charCountColor = charCount > 8000 ? 'text-red-400' : charCount > 5000 ? 'text-yellow-400' : 'text-white/60';

  return (
    <div className="h-full flex flex-col">
      <form onSubmit={handleSubmit} className="flex-1 flex flex-col">
        <div className="mb-6">
          <h3 className="text-2xl font-bold text-white mb-2">Analyze Text Content</h3>
          <p className="text-white/80">
            Paste news article text, social media post, or any content you want to verify.
          </p>
        </div>

        <div className="flex-1 relative">
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste the news article or content you want to analyze here...

Example: Breaking: Scientists discover that eating chocolate cures all diseases! Researchers at the University of Miracle Studies have found that consuming just one chocolate bar per day can prevent cancer, reverse aging, and make you smarter. The big pharmaceutical companies don't want you to know this shocking truth!"
            className="w-full h-64 p-4 bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl text-white placeholder-white/50 resize-none focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
            disabled={isAnalyzing}
          />
          
          {/* Character count */}
          <div className="absolute bottom-4 right-4">
            <span className={`text-sm ${charCountColor}`}>
              {charCount.toLocaleString()}/10,000
            </span>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center justify-between mt-6">
          <div className="flex items-center space-x-4">
            <button
              type="button"
              onClick={handleClear}
              disabled={isAnalyzing || !text}
              className="px-6 py-3 bg-white/10 text-white rounded-xl hover:bg-white/20 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              Clear
            </button>
            
            <div className="flex items-center space-x-2 text-white/60 text-sm">
              <FileText className="w-4 h-4" />
              <span>Supports multiple languages</span>
            </div>
          </div>

          <button
            type="submit"
            disabled={isAnalyzing || !text.trim() || text.length < 50}
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
                <span>Analyze Content</span>
              </>
            )}
          </button>
        </div>
      </form>

      {/* Tips */}
      <div className="mt-6 p-4 bg-blue-500/20 border border-blue-400/30 rounded-xl">
        <h4 className="text-white font-semibold mb-2 flex items-center">
          <Sparkles className="w-4 h-4 mr-2" />
          Pro Tips
        </h4>
        <ul className="text-white/80 text-sm space-y-1">
          <li>• Include the full article text for better accuracy</li>
          <li>• Longer texts provide more reliable analysis</li>
          <li>• Include headlines and subheadings for complete analysis</li>
          <li>• Multiple languages are supported (English, Hindi, Spanish, French, German)</li>
        </ul>
      </div>
    </div>
  );
};

export default TextInput;
