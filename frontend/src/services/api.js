import axios from 'axios';
import toast from 'react-hot-toast';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth-storage');
    if (token) {
      try {
        const authData = JSON.parse(token);
        if (authData.state?.token) {
          config.headers.Authorization = `Bearer ${authData.state.token}`;
        }
      } catch (error) {
        console.error('Error parsing auth token:', error);
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized - clear auth and redirect to login
      localStorage.removeItem('auth-storage');
      window.location.href = '/';
      toast.error('Session expired. Please login again.');
    } else if (error.response?.status >= 500) {
      toast.error('Server error. Please try again later.');
    } else if (error.code === 'ECONNABORTED') {
      toast.error('Request timeout. Please check your connection.');
    }
    
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: async (userData) => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },
  
  login: async (credentials) => {
    const response = await api.post('/auth/login', credentials);
    return response.data;
  },
  
  logout: async () => {
    const response = await api.post('/auth/logout');
    return response.data;
  },
  
  getProfile: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

// Analysis API
export const analysisAPI = {
  analyzeText: async (textData) => {
    const response = await api.post('/analyze/text', textData);
    return response.data;
  },
  
  analyzeURL: async (urlData) => {
    const response = await api.post('/analyze/url', urlData);
    return response.data;
  },
  
  analyzePDF: async (formData) => {
    const response = await api.post('/analyze/pdf', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
  
  getHistory: async (params = {}) => {
    const response = await api.get('/analyze/history', { params });
    return response.data;
  },
  
  getArticle: async (articleId) => {
    const response = await api.get(`/analyze/article/${articleId}`);
    return response.data;
  },
};

// Sources API
export const sourcesAPI = {
  getSources: async (params = {}) => {
    const response = await api.get('/sources', { params });
    return response.data;
  },
  
  getSourceByDomain: async (domain) => {
    const response = await api.get(`/sources/${domain}`);
    return response.data;
  },
  
  getTopReliable: async (limit = 20) => {
    const response = await api.get('/sources/top/reliable', { params: { limit } });
    return response.data;
  },
  
  getTopUnreliable: async (limit = 20) => {
    const response = await api.get('/sources/top/unreliable', { params: { limit } });
    return response.data;
  },
  
  getStats: async () => {
    const response = await api.get('/sources/stats/overview');
    return response.data;
  },
};

// Health check
export const healthAPI = {
  check: async () => {
    const response = await api.get('/health');
    return response.data;
  },
};

export default api;
