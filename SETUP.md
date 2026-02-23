# TruthLens AI - Setup Guide

This comprehensive setup guide will help you deploy TruthLens AI in various environments.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Development Setup](#development-setup)
4. [Production Setup](#production-setup)
5. [Database Setup](#database-setup)
6. [Environment Configuration](#environment-configuration)
7. [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

### System Requirements
- **OS**: Linux, macOS, or Windows (with WSL2)
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: Minimum 10GB free space
- **CPU**: Multi-core processor recommended

### Required Software
- **Docker**: 20.10+ and Docker Compose 2.0+
- **Git**: For version control
- **Node.js**: 18+ (for local development)
- **Python**: 3.11+ (for local development)

### Install Docker

#### Linux (Ubuntu/Debian)
```bash
# Update package index
sudo apt-get update

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt-get install docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

#### macOS
```bash
# Install using Homebrew
brew install --cask docker

# Or download Docker Desktop
# https://www.docker.com/products/docker-desktop
```

#### Windows
```powershell
# Install using Chocolatey
choco install docker-desktop

# Or download Docker Desktop
# https://www.docker.com/products/docker-desktop
```

## 🚀 Quick Start

### One-Click Deployment
```bash
# Clone the repository
git clone https://github.com/truthlens-ai/truthlens-ai.git
cd truthlens-ai

# Make deployment script executable
chmod +x deploy.sh

# Deploy all services
./deploy.sh deploy
```

This will:
- ✅ Create database backup
- ✅ Pull and build Docker images
- ✅ Start all services
- ✅ Run database migrations
- ✅ Perform health checks

### Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database Admin**: http://localhost:5050

## 🛠️ Development Setup

### Option 1: Docker Development (Recommended)
```bash
# Start development environment
./deploy.sh dev

# Or manually
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

### Option 2: Local Development

#### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

#### Database Setup (Local)
```bash
# Start PostgreSQL and Redis
docker-compose -f docker-compose.db.yml up -d

# Initialize database
cd database
python init_db.py
```

### Development Tools
- **pgAdmin**: http://localhost:5050 (admin@truthlens.com / admin)
- **Adminer**: http://localhost:8080 (development only)
- **Redis CLI**: `docker exec -it truthlens-redis-dev redis-cli`

## 🏭 Production Setup

### Environment Preparation
```bash
# Create production environment file
cp .env.example .env.production

# Edit production variables
nano .env.production
```

### Production Variables
```bash
# Security
SECRET_KEY=your-super-secure-secret-key-here
POSTGRES_PASSWORD=your-secure-db-password
REDIS_PASSWORD=your-secure-redis-password

# URLs
FRONTEND_URL=https://yourdomain.com
API_URL=https://api.yourdomain.com

# SSL (if using nginx)
SSL_CERT_PATH=/etc/nginx/ssl/cert.pem
SSL_KEY_PATH=/etc/nginx/ssl/key.pem

# Monitoring (optional)
GRAFANA_PASSWORD=your-grafana-password
```

### Production Deployment
```bash
# Deploy to production
./deploy.sh prod

# Or manually
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

### SSL Certificate Setup
```bash
# Create SSL directory
mkdir -p nginx/ssl

# Generate self-signed certificate (for testing)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/key.pem \
  -out nginx/ssl/cert.pem

# Or use Let's Encrypt (recommended)
certbot --nginx -d yourdomain.com -d api.yourdomain.com
```

## 🗄️ Database Setup

### PostgreSQL Configuration

#### Connection String Format
```
postgresql://username:password@host:port/database_name
```

#### Example Configurations
```bash
# Development
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/truthlens_db

# Production
DATABASE_URL=postgresql://truthlens_user:secure_password@db.example.com:5432/truthlens_prod
```

#### Database Initialization
```bash
# Run initialization script
cd database
python init_db.py

# Or using Alembic
cd backend
alembic upgrade head

# Create initial data
python -c "
from app.models.database import engine, Base
Base.metadata.create_all(bind=engine)
print('Database tables created successfully')
"
```

#### Database Backup & Restore
```bash
# Backup
docker exec truthlens-postgres pg_dump -U postgres truthlens_db > backup.sql

# Restore
docker exec -i truthlens-postgres psql -U postgres truthlens_db < backup.sql

# Automated backup (add to crontab)
0 2 * * * /path/to/deploy.sh backup
```

### Redis Configuration
```bash
# Connection String
REDIS_URL=redis://:password@host:port/database

# Example
REDIS_URL=redis://:redis123@localhost:6379/0

# Test connection
docker exec truthlens-redis redis-cli ping
```

## ⚙️ Environment Configuration

### Backend Environment Variables
```bash
# Core Settings
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/truthlens_db
REDIS_URL=redis://:redis123@localhost:6379/0
SECRET_KEY=your-secret-key-here
ENVIRONMENT=development

# API Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
API_HOST=0.0.0.0
API_PORT=8000

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log

# ML Model Settings
MODEL_PATH=./models_training/saved_models
BERT_MODEL_NAME=bert-base-uncased

# External APIs
GOOGLE_TRANSLATE_API_KEY=your-google-api-key
NEWS_API_KEY=your-news-api-key
```

### Frontend Environment Variables
```bash
# API Configuration
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENV=development

# Feature Flags
REACT_APP_ENABLE_ANALYTICS=false
REACT_APP_ENABLE_SENTRY=false

# Build Settings
GENERATE_SOURCEMAP=false
INLINE_RUNTIME_CHUNK=false
```

### Docker Environment Files
```bash
# .env (development)
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/truthlens_db
REDIS_URL=redis://:redis123@redis:6379/0
SECRET_KEY=dev-secret-key
ENVIRONMENT=development

# .env.production (production)
DATABASE_URL=postgresql://postgres:${POSTGRES_PASSWORD}@postgres:5432/truthlens_db
REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0
SECRET_KEY=${SECRET_KEY}
ENVIRONMENT=production
```

## 🔧 Advanced Configuration

### Nginx Configuration
```bash
# Custom nginx config
cp nginx/nginx.conf nginx/nginx.custom.conf

# Edit configuration
nano nginx/nginx.custom.conf

# Update docker-compose to use custom config
volumes:
  - ./nginx/nginx.custom.conf:/etc/nginx/nginx.conf:ro
```

### Resource Limits
```yaml
# docker-compose.prod.yml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G
```

### Monitoring Setup
```bash
# Enable monitoring profile
docker-compose --profile monitoring up -d

# Access monitoring tools
# Grafana: http://localhost:3001
# Prometheus: http://localhost:9090
```

## 🐛 Troubleshooting

### Common Issues

#### Docker Issues
```bash
# Permission denied
sudo usermod -aG docker $user
newgrp docker

# Port conflicts
docker-compose down
sudo lsof -i :8000
sudo lsof -i :3000

# Clean up Docker
docker system prune -a
docker volume prune
```

#### Database Issues
```bash
# Connection refused
docker-compose logs postgres

# Database not ready
docker exec truthlens-postgres pg_isready -U postgres

# Reset database
docker-compose down -v
docker-compose up -d postgres
```

#### Backend Issues
```bash
# Module not found
cd backend
pip install -r requirements.txt

# Model loading errors
mkdir -p models_training/saved_models
# Download pre-trained models to this directory

# Permission issues
chmod -R 755 models_training/
chmod -R 755 logs/
```

#### Frontend Issues
```bash
# Node modules issues
cd frontend
rm -rf node_modules package-lock.json
npm install

# Build failures
npm run build
# Check for errors in build output

# CORS errors
# Check CORS_ORIGINS in backend environment
```

### Performance Issues
```bash
# Slow API responses
docker stats  # Check resource usage
docker-compose logs backend  # Check for errors

# Database performance
docker exec truthlens-postgres psql -U postgres -d truthlens_db -c "
SELECT query, calls, total_time, mean_time 
FROM pg_stat_statements 
ORDER BY total_time DESC 
LIMIT 10;"
```

### Log Analysis
```bash
# Application logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Database logs
docker-compose logs -f postgres

# Nginx logs
docker exec truthlens-nginx tail -f /var/log/nginx/access.log
```

### Health Checks
```bash
# Check all services
./deploy.sh status

# Individual service health
curl http://localhost:8000/health
curl http://localhost:3000/health

# Database health
docker exec truthlens-postgres pg_isready -U postgres
```

## 📞 Support

If you encounter issues not covered in this guide:

1. **Check GitHub Issues**: [Existing Issues](https://github.com/truthlens-ai/truthlens-ai/issues)
2. **Create New Issue**: [Report Bug](https://github.com/truthlens-ai/truthlens-ai/issues/new)
3. **Join Discord**: [Community Support](https://discord.gg/truthlens)
4. **Email Support**: support@truthlens.ai

## 🔄 Updates & Maintenance

### Regular Maintenance
```bash
# Update dependencies
cd backend && pip install -r requirements.txt --upgrade
cd frontend && npm update

# Update Docker images
docker-compose pull

# Restart services
./deploy.sh deploy
```

### Backup Strategy
```bash
# Automated daily backup
0 2 * * * /path/to/deploy.sh backup

# Weekly full backup
0 3 * * 0 /path/to/deploy.sh backup && \
  aws s3 sync ./backups s3://truthlens-backups/
```

---

For additional help, refer to our [API Documentation](./API_DOCS.md) or [Project Report](./REPORT.md).
