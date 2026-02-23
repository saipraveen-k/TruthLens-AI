# TruthLens AI Browser Extension

A Chrome browser extension that brings real-time news credibility analysis to your browsing experience.

## 🌟 Features

### Real-time Analysis
- **Automatic Detection**: Automatically detects news articles and analyzes credibility
- **Floating Button**: Quick access analysis button on any page
- **Context Menu**: Right-click to analyze selected text or entire page
- **Instant Results**: Get credibility scores in under 3 seconds

### Smart Detection
- **News Site Recognition**: Identifies major news websites automatically
- **Content Extraction**: Intelligently extracts article title and content
- **Multi-language Support**: Analyzes content in multiple languages
- **Source Verification**: Checks against known reliable/unreliable sources

### Visual Feedback
- **Credibility Gauge**: Visual representation of credibility scores
- **Color-coded Results**: Green (high), Yellow (medium), Red (low)
- **Detailed Metrics**: Fake probability, bias level, emotional manipulation
- **Analysis History**: Track your analysis history

### User Experience
- **Non-intrusive**: Doesn't interfere with your browsing
- **Privacy-focused**: Local processing with optional cloud analysis
- **Customizable Settings**: Configure auto-analysis and notifications
- **Cross-platform**: Works on Windows, Mac, and Linux

## 🚀 Installation

### From Chrome Web Store (Recommended)
1. Visit the [Chrome Web Store](https://chrome.google.com/webstore/detail/truthlens-ai)
2. Click "Add to Chrome"
3. Grant necessary permissions
4. Start browsing with real-time analysis!

### Manual Installation (Development)
1. Download the extension files
2. Open Chrome and go to `chrome://extensions/`
3. Enable "Developer mode"
4. Click "Load unpacked"
5. Select the extension folder

## 🔧 Configuration

### Extension Settings
- **Auto-analysis**: Automatically analyze news articles
- **Notifications**: Show credibility notifications
- **API Key**: Connect to TruthLens AI Pro features
- **Theme**: Light/Dark mode support

### Privacy Settings
- **Data Collection**: Choose what data to share
- **Local Analysis**: Process content locally when possible
- **History Management**: Control analysis history storage

## 📊 How It Works

### 1. Content Detection
```javascript
// Automatically detects news content
const isNewsSite = checkDomain(url);
const articleContent = extractArticleContent();
```

### 2. Analysis Request
```javascript
// Sends content to TruthLens AI API
const result = await analyzeContent({
  text: articleContent,
  url: currentPageUrl,
  language: 'auto'
});
```

### 3. Result Display
```javascript
// Shows credibility score with visual indicators
displayCredibilityScore({
  score: 85.2,
  level: 'High',
  details: analysisDetails
});
```

## 🎯 Usage Examples

### Analyzing Current Page
1. Visit any news article
2. Click the floating TruthLens button
3. View credibility analysis instantly
4. Get detailed breakdown of factors

### Analyzing Selected Text
1. Select any text on a webpage
2. Right-click and choose "Analyze with TruthLens AI"
3. Get credibility assessment for selected content

### Using Context Menu
1. Right-click on any page
2. Select "Analyze this page with TruthLens AI"
3. View comprehensive analysis results

## 🔍 Analysis Features

### Credibility Scoring
- **0-40%**: Low credibility (likely fake news)
- **40-60%**: Moderate credibility (verify claims)
- **60-80%**: Good credibility (generally reliable)
- **80-100%**: High credibility (very reliable)

### Detection Factors
- **Fake News Detection**: BERT-based AI analysis
- **Bias Analysis**: Political leaning and loaded language
- **Emotional Manipulation**: Appeals to emotion vs. facts
- **Source Reliability**: Known source credibility ratings
- **Fact-checking**: Cross-reference with verified sources

### Explanation Features
- **Sentence Highlighting**: Identifies suspicious content
- **Pattern Detection**: Recognizes manipulation techniques
- **Confidence Scores**: Shows AI confidence levels
- **Detailed Reasons**: Explains why content is flagged

## 🛡️ Privacy & Security

### Data Protection
- **Local Processing**: Content processed locally when possible
- **Encrypted Transmission**: Secure API communication
- **No Tracking**: Doesn't track your browsing history
- **User Control**: You control what data is shared

### Permissions Required
- `activeTab`: Access current tab content for analysis
- `storage`: Save settings and analysis history
- `scripting`: Inject analysis scripts into pages
- `contextMenus`: Add right-click menu options
- `notifications`: Show analysis results

### Data Usage
- **Text Content**: Only analyzed content, not stored
- **URL Information**: Current page URL for context
- **Settings**: Local preferences and configuration
- **History**: Optional analysis history storage

## 🔧 Development

### Extension Structure
```
browser-extension/
├── manifest.json          # Extension configuration
├── background.js          # Service worker
├── content.js            # Content script
├── content.css           # Content styles
├── popup.html            # Extension popup
├── popup.js              # Popup logic
├── options.html          # Settings page
├── icons/               # Extension icons
└── lib/                 # Utility functions
```

### Building the Extension
```bash
# Install dependencies
npm install

# Build for development
npm run build:dev

# Build for production
npm run build:prod

# Package extension
npm run package
```

### Testing
```bash
# Run tests
npm test

# Run integration tests
npm run test:integration

# Test in different browsers
npm run test:chrome
npm run test:firefox
```

## 📈 Performance

### Metrics
- **Analysis Speed**: < 3 seconds average
- **Memory Usage**: < 50MB typical
- **CPU Impact**: < 5% during analysis
- **Network Usage**: Minimal, only for API calls
- **Battery Impact**: Low impact on laptop battery

### Optimization
- **Lazy Loading**: Components loaded when needed
- **Caching**: Results cached for similar content
- **Background Processing**: Non-blocking analysis
- **Resource Management**: Efficient memory usage

## 🐛 Troubleshooting

### Common Issues

#### Extension Not Working
1. Check if extension is enabled in `chrome://extensions/`
2. Verify permissions are granted
3. Try reloading the extension
4. Check for Chrome updates

#### Analysis Not Triggering
1. Ensure you're on a supported news site
2. Check if auto-analysis is enabled
3. Try manual analysis using floating button
4. Verify internet connection

#### Slow Performance
1. Clear extension cache
2. Disable other content-heavy extensions
3. Check system resources
4. Restart Chrome browser

#### API Errors
1. Verify API key is valid (Pro features)
2. Check internet connection
3. Try again later (API may be busy)
4. Contact support if issue persists

### Debug Mode
Enable debug mode to troubleshoot issues:
1. Go to extension settings
2. Enable "Debug Mode"
3. Check browser console for errors
4. Review extension logs

## 🔄 Updates & Maintenance

### Automatic Updates
- Extension updates automatically through Chrome Web Store
- Settings preserved during updates
- New features added regularly
- Bug fixes deployed promptly

### Manual Updates
1. Check for updates in extension settings
2. Download latest version from GitHub
3. Install manually in developer mode
4. Migrate settings if needed

## 🤝 Contributing

We welcome contributions! See our [Contributing Guidelines](../CONTRIBUTING.md) for details.

### How to Contribute
1. Fork the repository
2. Create feature branch
3. Make your changes
4. Add tests
5. Submit pull request

### Areas for Contribution
- **New Features**: Analysis improvements, UI enhancements
- **Bug Fixes**: Report and fix issues
- **Translations**: Help translate to other languages
- **Documentation**: Improve guides and examples

## 📞 Support

### Getting Help
- **Documentation**: [Extension Guide](https://docs.truthlens.ai/extension)
- **FAQ**: [Frequently Asked Questions](https://truthlens.ai/faq)
- **Issues**: [Report Bugs](https://github.com/truthlens-ai/truthlens-ai/issues)
- **Email**: extension@truthlens.ai

### Community
- **Discord**: [Join Community](https://discord.gg/truthlens)
- **Reddit**: [r/TruthLensAI](https://reddit.com/r/truthlensai)
- **Twitter**: [@TruthLensAI](https://twitter.com/truthlens_ai)

## 📄 License

This extension is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 🙏 Acknowledgments

- **Chrome Extensions API**: For browser integration
- **TruthLens AI API**: For analysis services
- **Open Source Community**: For inspiration and tools
- **Beta Testers**: For valuable feedback and suggestions

---

**Made with ❤️ by the TruthLens AI Team**

*Version 1.0.0 - January 2024*
