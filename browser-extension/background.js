// Background Service Worker for TruthLens AI Browser Extension

class TruthLensBackground {
  constructor() {
    this.apiBaseUrl = 'https://api.truthlens.ai';
    this.initializeEventListeners();
    this.initializeContextMenu();
  }

  initializeEventListeners() {
    // Extension installation
    chrome.runtime.onInstalled.addListener((details) => {
      if (details.reason === 'install') {
        this.handleInstall();
      } else if (details.reason === 'update') {
        this.handleUpdate();
      }
    });

    // Message handling from content scripts
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
      this.handleMessage(message, sender, sendResponse);
      return true; // Keep message channel open for async response
    });

    // Tab updates for automatic analysis
    chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
      if (changeInfo.status === 'complete' && tab.url) {
        this.handleTabUpdate(tabId, tab);
      }
    });
  }

  initializeContextMenu() {
    chrome.contextMenus.create({
      id: 'analyze-text',
      title: 'Analyze selected text with TruthLens AI',
      contexts: ['selection']
    });

    chrome.contextMenus.create({
      id: 'analyze-page',
      title: 'Analyze this page with TruthLens AI',
      contexts: ['page']
    });

    chrome.contextMenus.onClicked.addListener((info, tab) => {
      this.handleContextMenuClick(info, tab);
    });
  }

  async handleInstall() {
    // Set default settings
    chrome.storage.sync.set({
      autoAnalyze: true,
      showNotifications: true,
      apiKey: null,
      analysisHistory: []
    });

    // Open welcome page
    chrome.tabs.create({
      url: chrome.runtime.getURL('welcome.html')
    });

    // Show notification
    chrome.notifications.create({
      type: 'basic',
      iconUrl: chrome.runtime.getURL('icons/icon48.png'),
      title: 'TruthLens AI Installed',
      message: 'Start analyzing news credibility while you browse!'
    });
  }

  handleUpdate() {
    chrome.notifications.create({
      type: 'basic',
      iconUrl: chrome.runtime.getURL('icons/icon48.png'),
      title: 'TruthLens AI Updated',
      message: 'New features and improvements are available!'
    });
  }

  async handleMessage(message, sender, sendResponse) {
    try {
      switch (message.type) {
        case 'ANALYZE_TEXT':
          const textResult = await this.analyzeText(message.text);
          sendResponse({ success: true, data: textResult });
          break;

        case 'ANALYZE_URL':
          const urlResult = await this.analyzeUrl(message.url);
          sendResponse({ success: true, data: urlResult });
          break;

        case 'GET_SETTINGS':
          const settings = await this.getSettings();
          sendResponse({ success: true, data: settings });
          break;

        case 'SAVE_SETTINGS':
          await this.saveSettings(message.settings);
          sendResponse({ success: true });
          break;

        case 'GET_HISTORY':
          const history = await this.getHistory();
          sendResponse({ success: true, data: history });
          break;

        case 'SAVE_TO_HISTORY':
          await this.saveToHistory(message.analysis);
          sendResponse({ success: true });
          break;

        default:
          sendResponse({ success: false, error: 'Unknown message type' });
      }
    } catch (error) {
      console.error('Background script error:', error);
      sendResponse({ success: false, error: error.message });
    }
  }

  async handleContextMenuClick(info, tab) {
    if (info.menuItemId === 'analyze-text' && info.selectionText) {
      // Analyze selected text
      const result = await this.analyzeText(info.selectionText);
      this.showAnalysisResult(result, 'text');
    } else if (info.menuItemId === 'analyze-page') {
      // Analyze current page
      const result = await this.analyzeUrl(tab.url);
      this.showAnalysisResult(result, 'url');
    }
  }

  async handleTabUpdate(tabId, tab) {
    const settings = await this.getSettings();
    
    if (settings.autoAnalyze && this.isNewsSite(tab.url)) {
      // Wait a bit for page to fully load
      setTimeout(async () => {
        try {
          const result = await this.analyzeUrl(tab.url);
          
          // Send result to content script
          chrome.tabs.sendMessage(tabId, {
            type: 'ANALYSIS_RESULT',
            data: result
          });

          // Show notification if enabled
          if (settings.showNotifications) {
            this.showNotification(result);
          }
        } catch (error) {
          console.error('Auto-analysis failed:', error);
        }
      }, 3000);
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

  async analyzeText(text) {
    const settings = await this.getSettings();
    
    const response = await fetch(`${this.apiBaseUrl}/analyze/text`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': settings.apiKey ? `Bearer ${settings.apiKey}` : ''
      },
      body: JSON.stringify({
        text: text,
        language: 'auto'
      })
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    const result = await response.json();
    
    // Save to history
    await this.saveToHistory({
      type: 'text',
      input: text.substring(0, 100) + '...',
      result: result,
      timestamp: new Date().toISOString()
    });

    return result;
  }

  async analyzeUrl(url) {
    const settings = await this.getSettings();
    
    const response = await fetch(`${this.apiBaseUrl}/analyze/url`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': settings.apiKey ? `Bearer ${settings.apiKey}` : ''
      },
      body: JSON.stringify({
        url: url,
        extract_full_text: true
      })
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    const result = await response.json();
    
    // Save to history
    await this.saveToHistory({
      type: 'url',
      input: url,
      result: result,
      timestamp: new Date().toISOString()
    });

    return result;
  }

  async getSettings() {
    return new Promise((resolve) => {
      chrome.storage.sync.get({
        autoAnalyze: true,
        showNotifications: true,
        apiKey: null,
        theme: 'light'
      }, (result) => resolve(result));
    });
  }

  async saveSettings(settings) {
    return new Promise((resolve) => {
      chrome.storage.sync.set(settings, resolve);
    });
  }

  async getHistory() {
    return new Promise((resolve) => {
      chrome.storage.sync.get(['analysisHistory'], (result) => {
        resolve(result.analysisHistory || []);
      });
    });
  }

  async saveToHistory(analysis) {
    const history = await this.getHistory();
    const newHistory = [analysis, ...history.slice(0, 99)]; // Keep last 100
    
    chrome.storage.sync.set({ analysisHistory: newHistory });
  }

  showAnalysisResult(result, type) {
    // Open popup with results
    chrome.tabs.create({
      url: chrome.runtime.getURL(`result.html?type=${type}&data=${encodeURIComponent(JSON.stringify(result))}`)
    });
  }

  showNotification(result) {
    const credibility = result.credibility_score;
    let title, message, iconUrl;

    if (credibility >= 80) {
      title = 'High Credibility Content';
      message = `This content appears highly credible (${credibility.toFixed(1)}% score)`;
      iconUrl = chrome.runtime.getURL('icons/green-icon48.png');
    } else if (credibility >= 60) {
      title = 'Moderate Credibility';
      message = `This content has moderate credibility (${credibility.toFixed(1)}% score)`;
      iconUrl = chrome.runtime.getURL('icons/yellow-icon48.png');
    } else {
      title = 'Low Credibility Warning';
      message = `This content has low credibility (${credibility.toFixed(1)}% score) - be cautious`;
      iconUrl = chrome.runtime.getURL('icons/red-icon48.png');
    }

    chrome.notifications.create({
      type: 'basic',
      iconUrl: iconUrl,
      title: title,
      message: message,
      buttons: [
        { title: 'View Details' },
        { title: 'Dismiss' }
      ]
    });
  }
}

// Initialize the background service
const truthLensBackground = new TruthLensBackground();
