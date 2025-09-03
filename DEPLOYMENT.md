# MentorMind Deployment Guide

## Overview
This guide covers the complete deployment of the MentorMind AI-powered learning platform, including backend, frontend, database, and monitoring services.

## Prerequisites
- Docker and Docker Compose installed
- Python 3.11+ and Node.js 18+
- PostgreSQL 15+ (for local development)
- Redis 7+ (for caching)
- AWS CLI configured (for production deployment)

## Local Development Setup

### 1. Clone and Setup
```bash
git clone <repository-url>
cd MentorMind
cp env.example .env
# Edit .env with your local configuration
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-test.txt
```

### 3. Frontend Setup
```bash
cd student-portal
npm install
```

### 4. Database Setup
```bash
# Using Docker
docker run --name mentormind-postgres \
  -e POSTGRES_DB=mentormind \
  -e POSTGRES_USER=mentormind_user \
  -e POSTGRES_PASSWORD=mentormind_password \
  -p 5432:5432 \
  -d postgres:15-alpine

# Or using local PostgreSQL
createdb mentormind
psql -d mentormind -f database/init/01_init.sql
```

### 5. Run Tests
```bash
cd backend
python run_tests.py
```

### 6. Start Services
```bash
# Backend
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (in another terminal)
cd student-portal
npm run dev
```

## Docker Deployment

### 1. Build and Run with Docker Compose
```bash
# Build all services
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 2. Individual Service Management
```bash
# Start specific service
docker-compose up -d backend

# View service logs
docker-compose logs backend

# Restart service
docker-compose restart backend
```

## Production Deployment (AWS)

### 1. Infrastructure Setup
```bash
# Create EC2 instance
aws ec2 run-instances \
  --image-id ami-0c02fb55956c7d316 \
  --instance-type t3.medium \
  --key-name your-key-pair \
  --security-group-ids sg-xxxxxxxxx \
  --subnet-id subnet-xxxxxxxxx

# Create RDS PostgreSQL instance
aws rds create-db-instance \
  --db-instance-identifier mentormind-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username mentormind_user \
  --master-user-password mentormind_password \
  --allocated-storage 20
```

### 2. Server Configuration
```bash
# Connect to EC2 instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Install Docker
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 3. Application Deployment
```bash
# Clone repository
git clone <repository-url>
cd MentorMind

# Configure environment
cp env.example .env
# Edit .env with production values

# Build and start services
docker-compose -f docker-compose.prod.yml up -d

# Check service status
docker-compose ps
docker-compose logs -f
```

### 4. SSL Configuration
```bash
# Install Certbot
sudo yum install -y certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Monitoring and Logging

### 1. Prometheus + Grafana
```bash
# Add monitoring services to docker-compose
docker-compose -f docker-compose.monitoring.yml up -d
```

### 2. Log Management
```bash
# View application logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Log aggregation with ELK Stack
docker-compose -f docker-compose.logging.yml up -d
```

## Performance Optimization

### 1. Database Optimization
```sql
-- Add indexes for frequently queried fields
CREATE INDEX idx_student_progress_user_id ON student_progress(user_id);
CREATE INDEX idx_student_progress_subject ON student_progress(subject);
CREATE INDEX idx_student_progress_created_at ON student_progress(created_at);

-- Enable query optimization
ANALYZE student_progress;
```

### 2. Caching Strategy
```bash
# Redis configuration for caching
docker-compose exec redis redis-cli
> CONFIG SET maxmemory 256mb
> CONFIG SET maxmemory-policy allkeys-lru
```

### 3. Load Balancing
```bash
# Scale backend services
docker-compose up -d --scale backend=3

# Configure Nginx load balancer
# Edit nginx/nginx.conf for load balancing
```

## Security Configuration

### 1. Environment Variables
```bash
# Generate secure secret key
openssl rand -hex 32

# Update .env file
SECRET_KEY=your-generated-secret-key
DATABASE_URL=postgresql://user:password@host:port/db
```

### 2. Firewall Configuration
```bash
# Configure security groups
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxxxxxx \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxxxxxx \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0
```

### 3. SSL/TLS Configuration
```nginx
# Nginx SSL configuration
server {
    listen 443 ssl http2;
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
}
```

## Backup and Recovery

### 1. Database Backup
```bash
# Automated backup script
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec postgres pg_dump -U mentormind_user mentormind > $BACKUP_DIR/backup_$DATE.sql

# Add to crontab for daily backups
0 2 * * * /path/to/backup-script.sh
```

### 2. Application Backup
```bash
# Backup application data
tar -czf mentormind_backup_$(date +%Y%m%d).tar.gz \
  --exclude=node_modules \
  --exclude=venv \
  --exclude=.git \
  .
```

## Troubleshooting

### Common Issues

#### 1. Database Connection Issues
```bash
# Check database status
docker-compose exec postgres pg_isready -U mentormind_user

# Reset database
docker-compose down -v
docker-compose up -d postgres
```

#### 2. Memory Issues
```bash
# Check memory usage
docker stats

# Increase memory limits in docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 1G
```

#### 3. Performance Issues
```bash
# Monitor response times
docker-compose exec backend python -m locust -f locustfile.py

# Check slow queries
docker-compose exec postgres psql -U mentormind_user -d mentormind -c "SELECT * FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;"
```

## Support and Maintenance

### 1. Regular Maintenance
- Weekly: Check logs for errors
- Monthly: Update dependencies
- Quarterly: Security audit and penetration testing

### 2. Monitoring Alerts
- Set up CloudWatch alarms for CPU, memory, and disk usage
- Configure SNS notifications for critical alerts
- Monitor application metrics with custom dashboards

### 3. Update Procedures
```bash
# Update application
git pull origin main
docker-compose build
docker-compose up -d

# Rollback if needed
git checkout <previous-commit>
docker-compose up -d
```

## Contact and Support
For deployment support and issues:
- Create an issue in the GitHub repository
- Contact the development team
- Check the troubleshooting section above
