import React, { useState, useCallback } from 'react';
import { motion } from 'framer-motion';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, X, Sparkles, CheckCircle } from 'lucide-react';
import { useAnalysisStore } from '../../stores/authStore';
import { analysisAPI } from '../../services/api';
import toast from 'react-hot-toast';

const PDFUpload = ({ isAnalyzing, setIsAnalyzing }) => {
  const [files, setFiles] = useState([]);
  const { setAnalysis, addToHistory } = useAnalysisStore();

  const onDrop = useCallback((acceptedFiles) => {
    const filteredFiles = acceptedFiles.filter(file => file.type === 'application/pdf');
    
    if (filteredFiles.length === 0) {
      toast.error('Please upload only PDF files');
      return;
    }

    if (filteredFiles.length > 1) {
      toast.error('Please upload only one PDF file at a time');
      return;
    }

    const file = filteredFiles[0];
    
    // Check file size (10MB limit)
    if (file.size > 10 * 1024 * 1024) {
      toast.error('File size must be less than 10MB');
      return;
    }

    setFiles([file]);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    multiple: false,
    maxSize: 10 * 1024 * 1024, // 10MB
  });

  const removeFile = () => {
    setFiles([]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (files.length === 0) {
      toast.error('Please select a PDF file to analyze');
      return;
    }

    setIsAnalyzing(true);
    
    try {
      const formData = new FormData();
      formData.append('file', files[0]);
      
      const result = await analysisAPI.analyzePDF(formData);
      
      setAnalysis(result);
      addToHistory(result);
      
      toast.success('PDF analyzed successfully!');
      
      // Redirect to results
      window.location.href = '/dashboard';
      
    } catch (error) {
      console.error('Analysis error:', error);
      toast.error(error.response?.data?.detail || 'Failed to analyze PDF. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="h-full flex flex-col">
      <form onSubmit={handleSubmit} className="flex-1 flex flex-col">
        <div className="mb-6">
          <h3 className="text-2xl font-bold text-white mb-2">Upload PDF Document</h3>
          <p className="text-white/80">
            Upload a PDF file containing news articles or documents you want to verify.
          </p>
        </div>

        <div className="flex-1 space-y-4">
          {/* Dropzone */}
          <div
            {...getRootProps()}
            className={`relative border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all ${
              isDragActive
                ? 'border-purple-400 bg-purple-500/10'
                : 'border-white/30 bg-white/5 hover:border-white/50 hover:bg-white/10'
            } ${isAnalyzing ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            <input {...getInputProps()} disabled={isAnalyzing} />
            
            {files.length > 0 ? (
              <div className="space-y-4">
                <div className="flex items-center justify-center space-x-3 p-4 bg-green-500/20 border border-green-400/30 rounded-lg">
                  <CheckCircle className="w-6 h-6 text-green-400" />
                  <div className="text-left">
                    <p className="text-white font-medium">{files[0].name}</p>
                    <p className="text-white/60 text-sm">{formatFileSize(files[0].size)}</p>
                  </div>
                  <button
                    type="button"
                    onClick={removeFile}
                    disabled={isAnalyzing}
                    className="p-1 text-white/60 hover:text-white hover:bg-white/10 rounded transition-all"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="flex justify-center">
                  <Upload className="w-12 h-12 text-white/60" />
                </div>
                <div>
                  <p className="text-white font-medium mb-2">
                    {isDragActive ? 'Drop your PDF file here' : 'Drag & drop your PDF file here'}
                  </p>
                  <p className="text-white/60 text-sm">
                    or click to browse your files
                  </p>
                </div>
              </div>
            )}
          </div>

          {/* File Requirements */}
          <div className="p-4 bg-white/5 rounded-xl">
            <h4 className="text-white font-semibold mb-3 text-sm">File Requirements:</h4>
            <ul className="text-white/80 text-sm space-y-1">
              <li>• PDF format only (.pdf)</li>
              <li>• Maximum file size: 10MB</li>
              <li>• Text-based PDFs work best</li>
              <li>• Scanned images may not be readable</li>
            </ul>
          </div>

          {/* Sample Files */}
          <div className="p-4 bg-white/5 rounded-xl">
            <h4 className="text-white font-semibold mb-3 text-sm">Test with Sample Files:</h4>
            <div className="grid grid-cols-2 gap-2">
              <button
                type="button"
                className="text-left p-2 bg-white/10 hover:bg-white/20 rounded-lg text-white/80 hover:text-white text-sm transition-all"
              >
                📄 Sample News Article
              </button>
              <button
                type="button"
                className="text-left p-2 bg-white/10 hover:bg-white/20 rounded-lg text-white/80 hover:text-white text-sm transition-all"
              >
                📄 Sample Research Paper
              </button>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center justify-between mt-6">
          <div className="flex items-center space-x-4">
            {files.length > 0 && (
              <button
                type="button"
                onClick={removeFile}
                disabled={isAnalyzing}
                className="px-6 py-3 bg-white/10 text-white rounded-xl hover:bg-white/20 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                Remove File
              </button>
            )}
            
            <div className="flex items-center space-x-2 text-white/60 text-sm">
              <FileText className="w-4 h-4" />
              <span>Supports text extraction</span>
            </div>
          </div>

          <button
            type="submit"
            disabled={isAnalyzing || files.length === 0}
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
                <span>Analyze PDF</span>
              </>
            )}
          </button>
        </div>
      </form>

      {/* Tips */}
      <div className="mt-6 p-4 bg-purple-500/20 border border-purple-400/30 rounded-xl">
        <h4 className="text-white font-semibold mb-2 flex items-center">
          <Sparkles className="w-4 h-4 mr-2" />
          PDF Analysis Tips
        </h4>
        <ul className="text-white/80 text-sm space-y-1">
          <li>• Text-based PDFs provide the best results</li>
          <li>• Scanned documents may not be readable</li>
          <li>• Larger documents may take longer to process</li>
          <li>• Encrypted or password-protected PDFs are not supported</li>
        </ul>
      </div>
    </div>
  );
};

export default PDFUpload;
