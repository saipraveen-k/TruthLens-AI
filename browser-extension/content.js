// Content Script for TruthLens AI Browser Extension

class TruthLensContent {
  constructor() {
    this.isAnalyzing = false;
    this.currentAnalysis = null;
    this.initialize();
  }

  async initialize() {
    // Wait for page to load
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.setup());
    } else {
      this.setup();
    }

    // Listen for messages from background script
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
      this.handleMessage(message, sender, sendResponse);
    });
  }

  setup() {
    this.createFloatingButton();
    this.detectNewsContent();
  }

  createFloatingButton() {
    // Create floating analysis button
    const button = document.createElement('div');
    button.id = 'truthlens-floating-button';
    button.innerHTML = `
      <div class="tl-button">
        <img src="${chrome.runtime.getURL('icons/icon32.png')}" alt="TruthLens AI">
        <span>Analyze</span>
      </div>
    `;
    
    // Add styles
    button.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 10000;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    `;

    document.body.appendChild(button);

    // Add click handler
    button.querySelector('.tl-button').addEventListener('click', () => {
      this.analyzeCurrentPage();
    });
  }

  detectNewsContent() {
    // Try to detect if this is a news article
    const title = this.extractTitle();
    const content = this.extractContent();
    
    if (title && content && content.length > 100) {
      this.showContentIndicator();
    }
  }

  extractTitle() {
    const selectors = [
      'h1',
      '[property="og:title"]',
      '.article-title',
      '.headline',
      '.entry-title'
    ];

    for (const selector of selectors) {
      const element = document.querySelector(selector);
      if (element) {
        return element.textContent?.trim() || element.getAttribute('content');
      }
    }
    return document.title;
  }

  extractContent() {
    const selectors = [
      'article',
      '.article-content',
      '.entry-content',
      '.post-content',
      '.content',
      '[property="article:body"]'
    ];

    for (const selector of selectors) {
      const element = document.querySelector(selector);
      if (element) {
        return element.textContent?.trim();
      }
    }

    // Fallback to main content area
    const mainContent = document.querySelector('main') || document.querySelector('.main');
    return mainContent?.textContent?.trim() || '';
  }

  showContentIndicator() {
    // Show small indicator that content is detected
    const indicator = document.createElement('div');
    indicator.id = 'truthlens-content-indicator';
    indicator.innerHTML = `
      <div class="tl-indicator">
        <img src="${chrome.runtime.getURL('icons/icon16.png')}" alt="TruthLens">
        <span>News content detected</span>
      </div>
    `;
    
    indicator.style.cssText = `
      position: fixed;
      top: 20px;
      left: 20px;
      z-index: 10000;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    `;

    document.body.appendChild(indicator);

    // Auto-hide after 5 seconds
    setTimeout(() => {
      if (indicator.parentNode) {
        indicator.parentNode.removeChild(indicator);
      }
    }, 5000);
  }

  async analyzeCurrentPage() {
    if (this.isAnalyzing) return;

    this.isAnalyzing = true;
    this.showLoadingIndicator();

    try {
      const title = this.extractTitle();
      const content = this.extractContent();
      const url = window.location.href;

      // Send analysis request to background script
      const response = await chrome.runtime.sendMessage({
        type: 'ANALYZE_URL',
        url: url
      });

      if (response.success) {
        this.currentAnalysis = response.data;
        this.showAnalysisResult(response.data);
      } else {
        this.showError(response.error);
      }
    } catch (error) {
      this.showError(error.message);
    } finally {
      this.isAnalyzing = false;
      this.hideLoadingIndicator();
    }
  }

  showLoadingIndicator() {
    const loader = document.createElement('div');
    loader.id = 'truthlens-loader';
    loader.innerHTML = `
      <div class="tl-loader">
        <div class="tl-spinner"></div>
        <span>Analyzing content...</span>
      </div>
    `;
    
    loader.style.cssText = `
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      z-index: 10001;
      background: rgba(255, 255, 255, 0.95);
      padding: 20px;
      border-radius: 12px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      text-align: center;
    `;

    document.body.appendChild(loader);
  }

  hideLoadingIndicator() {
    const loader = document.getElementById('truthlens-loader');
    if (loader) {
      loader.parentNode.removeChild(loader);
    }
  }

  showAnalysisResult(analysis) {
    // Create analysis result popup
    const popup = document.createElement('div');
    popup.id = 'truthlens-result';
    
    const credibilityScore = analysis.credibility_score;
    const credibilityLevel = this.getCredibilityLevel(credibilityScore);
    const fakeProbability = analysis.fake_probability;

    popup.innerHTML = `
      <div class="tl-result">
        <div class="tl-header">
          <img src="${chrome.runtime.getURL('icons/icon48.png')}" alt="TruthLens AI">
          <h3>TruthLens AI Analysis</h3>
          <button class="tl-close">&times;</button>
        </div>
        
        <div class="tl-score">
          <div class="tl-gauge">
            <div class="tl-score-circle ${credibilityLevel.class}">
              <span class="tl-score-number">${credibilityScore.toFixed(1)}%</span>
            </div>
          </div>
          <div class="tl-score-text">
            <h4>${credibilityLevel.label}</h4>
            <p>${credibilityLevel.description}</p>
          </div>
        </div>

        <div class="tl-metrics">
          <div class="tl-metric">
            <span class="tl-label">Fake Probability</span>
            <span class="tl-value ${fakeProbability > 60 ? 'high' : 'normal'}">${fakeProbability.toFixed(1)}%</span>
          </div>
          <div class="tl-metric">
            <span class="tl-label">Bias Level</span>
            <span class="tl-value">${analysis.bias_score || 'N/A'}</span>
          </div>
          <div class="tl-metric">
            <span class="tl-label">Emotional Manipulation</span>
            <span class="tl-value">${analysis.emotional_manipulation || 'N/A'}</span>
          </div>
        </div>

        <div class="tl-actions">
          <button class="tl-btn tl-btn-primary" id="view-details">View Full Analysis</button>
          <button class="tl-btn tl-btn-secondary" id="share-result">Share Result</button>
        </div>
      </div>
    `;

    // Add styles
    popup.style.cssText = `
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      z-index: 10002;
      background: white;
      border-radius: 16px;
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      max-width: 400px;
      width: 90%;
    `;

    document.body.appendChild(popup);

    // Add event listeners
    popup.querySelector('.tl-close').addEventListener('click', () => {
      this.hideAnalysisResult();
    });

    popup.querySelector('#view-details').addEventListener('click', () => {
      this.openFullAnalysis(analysis);
    });

    popup.querySelector('#share-result').addEventListener('click', () => {
      this.shareResult(analysis);
    });

    // Close on outside click
    popup.addEventListener('click', (e) => {
      if (e.target === popup) {
        this.hideAnalysisResult();
      }
    });
  }

  hideAnalysisResult() {
    const popup = document.getElementById('truthlens-result');
    if (popup) {
      popup.parentNode.removeChild(popup);
    }
  }

  getCredibilityLevel(score) {
    if (score >= 80) {
      return {
        label: 'Highly Credible',
        class: 'high',
        description: 'This content appears highly credible and trustworthy'
      };
    } else if (score >= 60) {
      return {
        label: 'Moderately Credible',
        class: 'medium',
        description: 'This content appears moderately credible but verify important claims'
      };
    } else {
      return {
        label: 'Low Credibility',
        class: 'low',
        description: 'This content shows credibility concerns - exercise caution'
      };
    }
  }

  openFullAnalysis(analysis) {
    // Open full analysis in new tab
    chrome.runtime.sendMessage({
      type: 'OPEN_FULL_ANALYSIS',
      data: analysis
    });
  }

  shareResult(analysis) {
    const text = `TruthLens AI Analysis: ${analysis.credibility_score.toFixed(1)}% credibility score`;
    const url = `https://truthlens.ai/analysis/${analysis.article_id}`;
    
    if (navigator.share) {
      navigator.share({
        title: 'TruthLens AI Analysis',
        text: text,
        url: url
      });
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(`${text} - ${url}`);
      this.showToast('Analysis result copied to clipboard!');
    }
  }

  showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'truthlens-toast';
    toast.textContent = message;
    
    toast.style.cssText = `
      position: fixed;
      bottom: 20px;
      right: 20px;
      background: #333;
      color: white;
      padding: 12px 16px;
      border-radius: 8px;
      z-index: 10003;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      font-size: 14px;
    `;

    document.body.appendChild(toast);

    setTimeout(() => {
      if (toast.parentNode) {
        toast.parentNode.removeChild(toast);
      }
    }, 3000);
  }

  showError(message) {
    this.showToast(`Error: ${message}`);
  }

  handleMessage(message, sender, sendResponse) {
    if (message.type === 'ANALYSIS_RESULT') {
      this.currentAnalysis = message.data;
      this.showAnalysisResult(message.data);
    }
  }
}

// Initialize content script
const truthLensContent = new TruthLensContent();
