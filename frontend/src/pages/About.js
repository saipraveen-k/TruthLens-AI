import React from 'react';
import { motion } from 'framer-motion';
import { 
  Brain, 
  ShieldCheck, 
  Users, 
  Award, 
  BookOpen, 
  MessageSquare,
  Github,
  Twitter,
  Linkedin,
  Mail
} from 'lucide-react';

const About = () => {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        duration: 0.6,
        staggerChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        type: 'spring',
        stiffness: 100,
      },
    },
  };

  const team = [
    {
      name: 'K.SAI Praveen',
      role: 'Lead AI Engineer',
      avatar: '👨‍💻',
      contribution: 'BERT model, XAI implementation, Dataset curation'
    },
    {
      name: 'S.lakshmikanth Sai',
      role: 'ML Engineer', 
      avatar: '🧠',
      contribution: 'Bias detection, Emotion analysis, Model optimization'
    },
    {
      name: 'P.Reshma',
      role: 'Frontend Developer',
      avatar: '👩‍💻',
      contribution: 'React dashboard, UI/UX design, Visualizations'
    }
  ];

  const features = [
    {
      icon: <Brain className="w-8 h-8" />,
      title: 'Advanced AI Analysis',
      description: 'State-of-the-art BERT models analyze text for credibility, bias, and emotional manipulation with 94% accuracy.'
    },
    {
      icon: <ShieldCheck className="w-8 h-8" />,
      title: 'Explainable AI',
      description: 'Understand why content is flagged with highlighted suspicious sentences and detailed explanations.'
    },
    {
      icon: <Users className="w-8 h-8" />,
      title: 'Multi-language Support',
      description: 'Analyze content in English, Hindi, Spanish, French, and German with automatic translation.'
    },
    {
      icon: <Award className="w-8 h-8" />,
      title: 'Real-time Results',
      description: 'Get instant credibility analysis in under 3 seconds with comprehensive scoring breakdown.'
    }
  ];

  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={containerVariants}
      className="max-w-6xl mx-auto"
    >
      {/* Hero Section */}
      <motion.div variants={itemVariants} className="text-center mb-12">
        <div className="inline-flex items-center space-x-3 mb-6">
          <Brain className="w-12 h-12 text-purple-400" />
          <h1 className="text-5xl md:text-6xl font-bold gradient-text">About TruthLens AI</h1>
        </div>
        
        <p className="text-xl md:text-2xl text-white/90 mb-8 max-w-3xl mx-auto">
          Advanced AI-powered news credibility analyzer helping you detect misinformation, 
          analyze bias, and verify sources in real-time.
        </p>

        <div className="flex flex-wrap justify-center gap-6 mb-8">
          <div className="flex items-center space-x-2 bg-white/10 backdrop-blur-sm rounded-lg px-4 py-2">
            <ShieldCheck className="w-5 h-5 text-green-400" />
            <span className="text-white text-sm font-medium">94% Accuracy</span>
          </div>
          <div className="flex items-center space-x-2 bg-white/10 backdrop-blur-sm rounded-lg px-4 py-2">
            <Users className="w-5 h-5 text-blue-400" />
            <span className="text-white text-sm font-medium">10K+ Users</span>
          </div>
          <div className="flex items-center space-x-2 bg-white/10 backdrop-blur-sm rounded-lg px-4 py-2">
            <Award className="w-5 h-5 text-purple-400" />
            <span className="text-white text-sm font-medium">Hackathon Winner</span>
          </div>
        </div>
      </motion.div>

      {/* Mission Section */}
      <motion.div variants={itemVariants} className="glass-morphism rounded-2xl p-8 mb-8">
        <h2 className="text-3xl font-bold text-white mb-6 text-center">Our Mission</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="text-4xl mb-4">🎯</div>
            <h3 className="text-xl font-semibold text-white mb-3">Detect</h3>
            <p className="text-white/80">
              Identify misinformation and fake news with advanced AI algorithms
            </p>
          </div>
          <div className="text-center">
            <div className="text-4xl mb-4">🔍</div>
            <h3 className="text-xl font-semibold text-white mb-3">Analyze</h3>
            <p className="text-white/80">
              Examine bias, emotional manipulation, and source credibility
            </p>
          </div>
          <div className="text-center">
            <div className="text-4xl mb-4">🛡️</div>
            <h3 className="text-xl font-semibold text-white mb-3">Trust</h3>
            <p className="text-white/80">
              Help users make informed decisions with reliable information
            </p>
          </div>
        </div>
      </motion.div>

      {/* Features Section */}
      <motion.div variants={itemVariants} className="mb-12">
        <h2 className="text-3xl font-bold text-center mb-8 gradient-text">Key Features</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {features.map((feature, index) => (
            <div key={index} className="glass-morphism rounded-2xl p-6 hover:scale-105 transition-all">
              <div className="flex items-start space-x-4">
                <div className="p-3 bg-gradient-to-r from-purple-500 to-blue-500 rounded-xl text-white">
                  {feature.icon}
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-white mb-3">{feature.title}</h3>
                  <p className="text-white/80">{feature.description}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </motion.div>

      {/* Team Section */}
      <motion.div variants={itemVariants} className="glass-morphism rounded-2xl p-8 mb-12">
        <h2 className="text-3xl font-bold text-center mb-8 gradient-text">Meet Our Team</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {team.map((member, index) => (
            <div key={index} className="text-center">
              <div className="text-6xl mb-4">{member.avatar}</div>
              <h3 className="text-xl font-semibold text-white mb-2">{member.name}</h3>
              <p className="text-purple-400 font-medium mb-3">{member.role}</p>
              <p className="text-white/70 text-sm">{member.contribution}</p>
            </div>
          ))}
        </div>
      </motion.div>

      {/* Technology Stack */}
      <motion.div variants={itemVariants} className="glass-morphism rounded-2xl p-8 mb-12">
        <h2 className="text-3xl font-bold text-center mb-8 gradient-text">Technology Stack</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <h3 className="text-xl font-semibold text-white mb-4 flex items-center">
              <Brain className="w-5 h-5 mr-2" />
              Backend
            </h3>
            <ul className="space-y-2 text-white/80">
              <li>• FastAPI (Python)</li>
              <li>• BERT & Transformers</li>
              <li>• PostgreSQL Database</li>
              <li>• PyTorch & Scikit-learn</li>
              <li>• Docker & Kubernetes</li>
            </ul>
          </div>
          <div>
            <h3 className="text-xl font-semibold text-white mb-4 flex items-center">
              <BookOpen className="w-5 h-5 mr-2" />
              Frontend
            </h3>
            <ul className="space-y-2 text-white/80">
              <li>• React with Next.js</li>
              <li>• Tailwind CSS</li>
              <li>• Framer Motion</li>
              <li>• Recharts & D3.js</li>
              <li>• Zustand State Management</li>
            </ul>
          </div>
        </div>
      </motion.div>

      {/* Contact Section */}
      <motion.div variants={itemVariants} className="text-center">
        <div className="glass-morphism rounded-2xl p-8 bg-gradient-to-r from-purple-600/20 to-blue-600/20">
          <h2 className="text-3xl font-bold gradient-text mb-4">Get In Touch</h2>
          <p className="text-xl text-white/90 mb-8 max-w-2xl mx-auto">
            Have questions about TruthLens AI? Want to contribute? We'd love to hear from you!
          </p>
          
          <div className="flex justify-center space-x-6 mb-8">
            <a
              href="https://github.com/truthlens-ai"
              target="_blank"
              rel="noopener noreferrer"
              className="p-3 bg-white/10 hover:bg-white/20 rounded-xl transition-all hover:scale-110"
            >
              <Github className="w-6 h-6 text-white" />
            </a>
            <a
              href="https://twitter.com/truthlens_ai"
              target="_blank"
              rel="noopener noreferrer"
              className="p-3 bg-white/10 hover:bg-white/20 rounded-xl transition-all hover:scale-110"
            >
              <Twitter className="w-6 h-6 text-white" />
            </a>
            <a
              href="https://linkedin.com/company/truthlens-ai"
              target="_blank"
              rel="noopener noreferrer"
              className="p-3 bg-white/10 hover:bg-white/20 rounded-xl transition-all hover:scale-110"
            >
              <Linkedin className="w-6 h-6 text-white" />
            </a>
            <a
              href="mailto:contact@truthlens.ai"
              className="p-3 bg-white/10 hover:bg-white/20 rounded-xl transition-all hover:scale-110"
            >
              <Mail className="w-6 h-6 text-white" />
            </a>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="px-8 py-3 bg-gradient-to-r from-purple-500 to-blue-500 text-white rounded-xl font-semibold hover:scale-105 transition-all">
              <MessageSquare className="w-5 h-5 mr-2" />
              Contact Support
            </button>
            <button className="px-8 py-3 bg-white/10 hover:bg-white/20 text-white rounded-xl font-semibold hover:scale-105 transition-all">
              <BookOpen className="w-5 h-5 mr-2" />
              View Documentation
            </button>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
};

export default About;
