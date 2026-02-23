import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useAuthStore = create(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      
      login: (userData, token) => {
        set({
          user: userData,
          token: token,
          isAuthenticated: true,
        });
      },
      
      logout: () => {
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        });
      },
      
      updateUser: (userData) => {
        set({ user: userData });
      },
    }),
    {
      name: 'auth-storage',
    }
  )
);

export const useAnalysisStore = create((set, get) => ({
  currentAnalysis: null,
  analysisHistory: [],
  isAnalyzing: false,
  
  setAnalysis: (analysis) => {
    set({ currentAnalysis: analysis });
  },
  
  addToHistory: (analysis) => {
    const { analysisHistory } = get();
    set({
      analysisHistory: [analysis, ...analysisHistory.slice(0, 49)], // Keep last 50
    });
  },
  
  setAnalyzing: (isAnalyzing) => {
    set({ isAnalyzing });
  },
  
  clearHistory: () => {
    set({ analysisHistory: [] });
  },
}));

export const useUIStore = create((set) => ({
  theme: 'light',
  sidebarOpen: false,
  
  toggleTheme: () => {
    set((state) => ({
      theme: state.theme === 'light' ? 'dark' : 'light',
    }));
  },
  
  toggleSidebar: () => {
    set((state) => ({
      sidebarOpen: !state.sidebarOpen,
    }));
  },
  
  setSidebarOpen: (open) => {
    set({ sidebarOpen: open });
  },
}));
