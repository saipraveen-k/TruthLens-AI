import React from 'react';
import { Brain, Github, Twitter, Linkedin, Mail } from 'lucide-react';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="glass-morphism rounded-2xl p-8 mt-16">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
        {/* Brand */}
        <div className="md:col-span-1">
          <div className="flex items-center space-x-3 mb-4">
            <div className="p-2 bg-gradient-to-r from-purple-500 to-blue-500 rounded-xl">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-xl font-bold gradient-text">TruthLens AI</h3>
          </div>
          <p className="text-white/80 text-sm mb-4">
            Advanced AI-powered news credibility analyzer helping you detect misinformation and bias.
          </p>
          <p className="text-white/60 text-xs">
            Detect. Analyze. Trust.
          </p>
        </div>

        {/* Quick Links */}
        <div>
          <h4 className="text-white font-semibold mb-4">Quick Links</h4>
          <ul className="space-y-2">
            <li>
              <a href="/" className="text-white/80 hover:text-white transition-colors text-sm">
                Home
              </a>
            </li>
            <li>
              <a href="/dashboard" className="text-white/80 hover:text-white transition-colors text-sm">
                Dashboard
              </a>
            </li>
            <li>
              <a href="/history" className="text-white/80 hover:text-white transition-colors text-sm">
                Analysis History
              </a>
            </li>
            <li>
              <a href="/about" className="text-white/80 hover:text-white transition-colors text-sm">
                About Us
              </a>
            </li>
          </ul>
        </div>

        {/* Resources */}
        <div>
          <h4 className="text-white font-semibold mb-4">Resources</h4>
          <ul className="space-y-2">
            <li>
              <a href="/docs" className="text-white/80 hover:text-white transition-colors text-sm">
                API Documentation
              </a>
            </li>
            <li>
              <a href="/research" className="text-white/80 hover:text-white transition-colors text-sm">
                Research Papers
              </a>
            </li>
            <li>
              <a href="/blog" className="text-white/80 hover:text-white transition-colors text-sm">
                Blog
              </a>
            </li>
            <li>
              <a href="/support" className="text-white/80 hover:text-white transition-colors text-sm">
                Support
              </a>
            </li>
          </ul>
        </div>

        {/* Connect */}
        <div>
          <h4 className="text-white font-semibold mb-4">Connect With Us</h4>
          <p className="text-white/80 text-sm mb-4">
            Stay updated with our latest features and research.
          </p>
          <div className="flex space-x-3">
            <a
              href="https://github.com/truthlens-ai"
              target="_blank"
              rel="noopener noreferrer"
              className="p-2 bg-white/10 hover:bg-white/20 rounded-lg transition-all hover:scale-110"
            >
              <Github className="w-5 h-5 text-white" />
            </a>
            <a
              href="https://twitter.com/truthlens_ai"
              target="_blank"
              rel="noopener noreferrer"
              className="p-2 bg-white/10 hover:bg-white/20 rounded-lg transition-all hover:scale-110"
            >
              <Twitter className="w-5 h-5 text-white" />
            </a>
            <a
              href="https://linkedin.com/company/truthlens-ai"
              target="_blank"
              rel="noopener noreferrer"
              className="p-2 bg-white/10 hover:bg-white/20 rounded-lg transition-all hover:scale-110"
            >
              <Linkedin className="w-5 h-5 text-white" />
            </a>
            <a
              href="mailto:contact@truthlens.ai"
              className="p-2 bg-white/10 hover:bg-white/20 rounded-lg transition-all hover:scale-110"
            >
              <Mail className="w-5 h-5 text-white" />
            </a>
          </div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="mt-8 pt-8 border-t border-white/20">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <p className="text-white/60 text-sm mb-4 md:mb-0">
            © {currentYear} TruthLens AI. All rights reserved.
          </p>
          <div className="flex space-x-6">
            <a href="/privacy" className="text-white/60 hover:text-white text-sm transition-colors">
              Privacy Policy
            </a>
            <a href="/terms" className="text-white/60 hover:text-white text-sm transition-colors">
              Terms of Service
            </a>
            <a href="/cookies" className="text-white/60 hover:text-white text-sm transition-colors">
              Cookie Policy
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
