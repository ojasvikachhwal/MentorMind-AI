#!/bin/bash

# MentorMind AI Learning Platform Startup Script
# This script helps you get the platform up and running quickly

echo "🚀 Welcome to MentorMind AI Learning Platform!"
echo "=============================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first:"
    echo "   https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first:"
    echo "   https://docs.docker.com/compose/install/"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating environment file..."
    if [ -f env.example ]; then
        cp env.example .env
        echo "✅ Environment file created from template."
        echo "   Please edit .env file with your configuration before continuing."
        echo ""
        read -p "Press Enter after editing .env file..."
    else
        echo "❌ env.example file not found. Please create .env file manually."
        exit 1
    fi
fi

echo "🔧 Starting MentorMind services..."
echo ""

# Start services
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service status
echo "📊 Service Status:"
echo "=================="

# Check PostgreSQL
if docker-compose ps postgres | grep -q "Up"; then
    echo "✅ PostgreSQL: Running"
else
    echo "❌ PostgreSQL: Not running"
fi

# Check Redis
if docker-compose ps redis | grep -q "Up"; then
    echo "✅ Redis: Running"
else
    echo "❌ Redis: Not running"
fi

# Check Backend
if docker-compose ps backend | grep -q "Up"; then
    echo "✅ Backend: Running"
else
    echo "❌ Backend: Not running"
fi

# Check Frontend
if docker-compose ps frontend | grep -q "Up"; then
    echo "✅ Frontend: Running"
else
    echo "❌ Frontend: Not running"
fi

echo ""
echo "🎉 MentorMind is starting up!"
echo ""
echo "📱 Access your application:"
echo "   Frontend: http://localhost:4200"
echo "   Backend API: http://localhost:8000"
echo "   API Documentation: http://localhost:8000/docs"
echo ""
echo "📚 Useful commands:"
echo "   View logs: docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart: docker-compose restart"
echo "   Rebuild: docker-compose up -d --build"
echo ""
echo "🔍 Troubleshooting:"
echo "   If services fail to start, check the logs:"
echo "   docker-compose logs [service-name]"
echo ""
echo "Happy learning! 🧠✨"
