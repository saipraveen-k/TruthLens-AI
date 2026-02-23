#!/bin/bash

# TruthLens AI Deployment Script
# Production deployment automation

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="truthlens"
BACKUP_DIR="./backups"
LOG_FILE="./logs/deployment.log"

# Create necessary directories
mkdir -p $BACKUP_DIR
mkdir -p ./logs

# Logging function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a $LOG_FILE
}

# Print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
    print_status "Docker is running"
}

# Backup database
backup_database() {
    print_step "Creating database backup..."
    
    BACKUP_FILE="$BACKUP_DIR/db_backup_$(date +%Y%m%d_%H%M%S).sql"
    
    docker exec truthlens-postgres pg_dump -U postgres truthlens_db > $BACKUP_FILE
    
    if [ $? -eq 0 ]; then
        print_status "Database backup created: $BACKUP_FILE"
    else
        print_error "Failed to create database backup"
        exit 1
    fi
}

# Pull latest images
pull_images() {
    print_step "Pulling latest Docker images..."
    
    docker-compose pull
    
    if [ $? -eq 0 ]; then
        print_status "Images pulled successfully"
    else
        print_error "Failed to pull images"
        exit 1
    fi
}

# Build custom images
build_images() {
    print_step "Building custom Docker images..."
    
    docker-compose build --no-cache
    
    if [ $? -eq 0 ]; then
        print_status "Images built successfully"
    else
        print_error "Failed to build images"
        exit 1
    fi
}

# Stop services
stop_services() {
    print_step "Stopping existing services..."
    
    docker-compose down
    
    if [ $? -eq 0 ]; then
        print_status "Services stopped successfully"
    else
        print_warning "Some services may not have been running"
    fi
}

# Start services
start_services() {
    print_step "Starting services..."
    
    docker-compose up -d
    
    if [ $? -eq 0 ]; then
        print_status "Services started successfully"
    else
        print_error "Failed to start services"
        exit 1
    fi
}

# Wait for services to be healthy
wait_for_services() {
    print_step "Waiting for services to be healthy..."
    
    # Wait for PostgreSQL
    print_status "Waiting for PostgreSQL..."
    until docker exec truthlens-postgres pg_isready -U postgres -d truthlens_db; do
        sleep 2
    done
    
    # Wait for Redis
    print_status "Waiting for Redis..."
    until docker exec truthlens-redis redis-cli ping; do
        sleep 2
    done
    
    # Wait for Backend
    print_status "Waiting for Backend API..."
    until curl -f http://localhost:8000/health; do
        sleep 5
    done
    
    # Wait for Frontend
    print_status "Waiting for Frontend..."
    until curl -f http://localhost:3000/health; do
        sleep 5
    done
    
    print_status "All services are healthy"
}

# Run database migrations
run_migrations() {
    print_step "Running database migrations..."
    
    docker exec truthlens-backend python -m alembic upgrade head
    
    if [ $? -eq 0 ]; then
        print_status "Database migrations completed"
    else
        print_error "Database migrations failed"
        exit 1
    fi
}

# Cleanup old images and containers
cleanup() {
    print_step "Cleaning up old Docker resources..."
    
    docker image prune -f
    docker container prune -f
    
    print_status "Cleanup completed"
}

# Show service status
show_status() {
    print_step "Service Status:"
    docker-compose ps
    
    echo ""
    print_step "Service URLs:"
    echo -e "${GREEN}Frontend:${NC} http://localhost:3000"
    echo -e "${GREEN}Backend API:${NC} http://localhost:8000"
    echo -e "${GREEN}API Documentation:${NC} http://localhost:8000/docs"
    echo -e "${GREEN}pgAdmin:${NC} http://localhost:5050"
}

# Main deployment function
deploy() {
    log "Starting deployment..."
    
    print_status "Starting TruthLens AI deployment..."
    
    check_docker
    backup_database
    stop_services
    pull_images
    build_images
    start_services
    wait_for_services
    run_migrations
    cleanup
    show_status
    
    print_status "Deployment completed successfully!"
    log "Deployment completed successfully"
}

# Development setup
dev_setup() {
    print_status "Setting up development environment..."
    
    check_docker
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
    
    print_status "Development environment started"
    show_status
}

# Production setup
prod_setup() {
    print_status "Setting up production environment..."
    
    check_docker
    backup_database
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
    
    print_status "Production environment started"
    show_status
}

# Show help
show_help() {
    echo "TruthLens AI Deployment Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  deploy      - Full deployment (backup, build, start, migrate)"
    echo "  dev         - Start development environment"
    echo "  prod        - Start production environment"
    echo "  backup      - Create database backup only"
    echo "  status      - Show service status"
    echo "  stop        - Stop all services"
    echo "  logs        - Show service logs"
    echo "  cleanup     - Clean up Docker resources"
    echo "  help        - Show this help message"
    echo ""
}

# Parse command line arguments
case "${1:-deploy}" in
    "deploy")
        deploy
        ;;
    "dev")
        dev_setup
        ;;
    "prod")
        prod_setup
        ;;
    "backup")
        backup_database
        ;;
    "status")
        show_status
        ;;
    "stop")
        stop_services
        ;;
    "logs")
        docker-compose logs -f
        ;;
    "cleanup")
        cleanup
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
