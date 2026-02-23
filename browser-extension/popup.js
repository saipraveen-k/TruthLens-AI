// Popup Script for TruthLens AI Browser Extension

class TruthLensPopup {
  constructor() {
    this.initialize();
  }

  async initialize() {
    // Load recent analyses
    await this.loadRecentAnalyses();
    
    // Setup event listeners
    this.setupEventListeners();
    
    // Check current tab
    await this.checkCurrentTab();
  }

  setupEventListeners() {
    document.getElementById('analyze-page').addEventListener('click', () => {
      this.analyzeCurrentPage();
    });

    document.getElementById('analyze-text').addEventListener('click', () => {
      this.analyzeSelectedText();
    });

    document.getElementById('open-dashboard').addEventListener('click', () => {
      this.openDashboard();
    });

    document.getElementById('settings').addEventListener('click', () => {
      this.openSettings();
    });
  }

  async loadRecentAnalyses() {
    try {
      const response = await chrome.runtime.sendMessage({ type: 'GET_HISTORY' });
      
      if (response.success && response.data.length > 0) {
        this.displayRecentAnalyses(response.data.slice(0, 3)); // Show last 3
      }
    } catch (error) {
      console.error('Failed to load recent analyses:', error);
    }
  }

  displayRecentAnalyses(analyses) {
    const recentSection = document.getElementById('recent-analysis');
    const recentList = document.getElementById('recent-list');
    
    if (analyses.length === 0) {
      return;
    }

    recentSection.style.display = 'block';
    recentList.innerHTML = '';

    analyses.forEach(analysis => {
      const item = this.createRecentAnalysisItem(analysis);
      recentList.appendChild(item);
    });
  }

  createRecentAnalysisItem(analysis) {
    const item = document.createElement('div');
    item.className = 'recent-item';
    
    const score = analysis.result.credibility_score;
    const scoreClass = score >= 80 ? 'high' : score >= 60 ? 'medium' : 'low';
    const scoreText = score.toFixed(0) + '%';
    
    const title = analysis.input.length > 30 
      ? analysis.input.substring(0, 30) + '...' 
      : analysis.input;
    
    const time = this.formatTime(analysis.timestamp);

    item.innerHTML = `
      <div class="recent-score ${scoreClass}">${scoreText}</div>
      <div class="recent-info">
        <div class="recent-title-text">${title}</div>
        <div class="recent-time">${time}</div>
      </div>
    `;

    item.addEventListener('click', () => {
      this.viewAnalysis(analysis);
    });

    return item;
  }

  formatTime(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    
    return date.toLocaleDateString();
  }

  async checkCurrentTab() {
    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      
      if (tab && tab.url) {
        // Check if it's a news site
        const isNewsSite = this.isNewsSite(tab.url);
        const analyzeBtn = document.getElementById('analyze-page');
        
        if (!isNewsSite) {
          analyzeBtn.style.opacity = '0.5';
          analyzeBtn.querySelector('.btn-description').textContent = 'Not a news site';
        }
      }
    } catch (error) {
      console.error('Failed to check current tab:', error);
    }
  }

  isNewsSite(url) {
    const newsDomains = [
      'cnn.com', 'bbc.com', 'reuters.com', 'foxnews.com', 'msnbc.com',
      'washingtonpost.com', 'nytimes.com', 'wsj.com', 'theguardian.com',
      'npr.org', 'ap.org', 'news.yahoo.com', 'google.com/news'
    ];
    
    try {
      const domain = new URL(url).hostname;
      return newsDomains.some(newsDomain => domain.includes(newsDomain));
    } catch {
      return false;
    }
  }

  async analyzeCurrentPage() {
    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      
      if (tab && tab.url) {
        // Send analysis request to background script
        const response = await chrome.runtime.sendMessage({
          type: 'ANALYZE_URL',
          url: tab.url
        });

        if (response.success) {
          this.showAnalysisResult(response.data);
        } else {
          this.showError(response.error);
        }
      }
    } catch (error) {
      this.showError('Failed to analyze page: ' + error.message);
    }
  }

  async analyzeSelectedText() {
    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      
      if (tab) {
        // Get selected text from content script
        const results = await chrome.scripting.executeScript({
          target: { tabId: tab.id },
          function: () => window.getSelection().toString()
        });

        const selectedText = results[0];
        
        if (!selectedText || selectedText.trim().length === 0) {
          this.showError('Please select some text first');
          return;
        }

        if (selectedText.length < 50) {
          this.showError('Selected text is too short (minimum 50 characters)');
          return;
        }

        // Send analysis request
        const response = await chrome.runtime.sendMessage({
          type: 'ANALYZE_TEXT',
          text: selectedText
        });

        if (response.success) {
          this.showAnalysisResult(response.data);
        } else {
          this.showError(response.error);
        }
      }
    } catch (error) {
      this.showError('Failed to analyze text: ' + error.message);
    }
  }

  openDashboard() {
    chrome.tabs.create({
      url: 'https://truthlens.ai/dashboard'
    });
  }

  openSettings() {
    chrome.tabs.create({
      url: chrome.runtime.getURL('options.html')
    });
  }

  viewAnalysis(analysis) {
    chrome.tabs.create({
      url: `https://truthlens.ai/analysis/${analysis.result.article_id}`
    });
  }

  showAnalysisResult(result) {
    // Create a simple result display
    const popup = document.createElement('div');
    popup.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.8);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 10000;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    `;

    const credibilityScore = result.credibility_score;
    const credibilityLevel = credibilityScore >= 80 ? 'High' : 
                          credibilityScore >= 60 ? 'Medium' : 'Low';
    const credibilityColor = credibilityScore >= 80 ? '#22c55e' : 
                           credibilityScore >= 60 ? '#f59e0b' : '#ef4444';

    popup.innerHTML = `
      <div style="background: white; padding: 30px; border-radius: 16px; max-width: 400px; text-align: center;">
        <h3 style="margin: 0 0 20px 0; color: #333;">Analysis Complete</h3>
        <div style="font-size: 48px; font-weight: bold; color: ${credibilityColor}; margin-bottom: 10px;">
          ${credibilityScore.toFixed(1)}%
        </div>
        <div style="font-size: 18px; color: #666; margin-bottom: 20px;">
          ${credibilityLevel} Credibility
        </div>
        <button onclick="this.parentElement.parentElement.remove()" style="
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border: none;
          padding: 12px 24px;
          border-radius: 8px;
          font-size: 14px;
          font-weight: 500;
          cursor: pointer;
        ">Close</button>
      </div>
    `;

    document.body.appendChild(popup);
  }

  showError(message) {
    const error = document.createElement('div');
    error.style.cssText = `
      position: fixed;
      top: 20px;
      left: 50%;
      transform: translateX(-50%);
      background: #ef4444;
      color: white;
      padding: 12px 20px;
      border-radius: 8px;
      z-index: 10000;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      font-size: 14px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    `;
    error.textContent = message;

    document.body.appendChild(error);

    setTimeout(() => {
      if (error.parentNode) {
        error.parentNode.removeChild(error);
      }
    }, 3000);
  }
}

// Initialize popup when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new TruthLensPopup();
});
