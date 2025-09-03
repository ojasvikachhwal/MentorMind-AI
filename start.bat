@echo off
chcp 65001 >nul
echo 🚀 Welcome to MentorMind AI Learning Platform!
echo ==============================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker first:
    echo    https://docs.docker.com/get-docker/
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first:
    echo    https://docs.docker.com/compose/install/
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo 📝 Creating environment file...
    if exist env.example (
        copy env.example .env >nul
        echo ✅ Environment file created from template.
        echo    Please edit .env file with your configuration before continuing.
        echo.
        pause
    ) else (
        echo ❌ env.example file not found. Please create .env file manually.
        pause
        exit /b 1
    )
)

echo 🔧 Starting MentorMind services...
echo.

REM Start services
docker-compose up -d

REM Wait for services to be ready
echo ⏳ Waiting for services to be ready...
timeout /t 10 /nobreak >nul

REM Check service status
echo 📊 Service Status:
echo ==================

REM Check PostgreSQL
docker-compose ps postgres | findstr "Up" >nul
if %errorlevel% equ 0 (
    echo ✅ PostgreSQL: Running
) else (
    echo ❌ PostgreSQL: Not running
)

REM Check Redis
docker-compose ps redis | findstr "Up" >nul
if %errorlevel% equ 0 (
    echo ✅ Redis: Running
) else (
    echo ❌ Redis: Not running
)

REM Check Backend
docker-compose ps backend | findstr "Up" >nul
if %errorlevel% equ 0 (
    echo ✅ Backend: Running
) else (
    echo ❌ Backend: Not running
)

REM Check Frontend
docker-compose ps frontend | findstr "Up" >nul
if %errorlevel% equ 0 (
    echo ✅ Frontend: Running
) else (
    echo ❌ Frontend: Not running
)

echo.
echo 🎉 MentorMind is starting up!
echo.
echo 📱 Access your application:
echo    Frontend: http://localhost:4200
echo    Backend API: http://localhost:8000
echo    API Documentation: http://localhost:8000/docs
echo.
echo 📚 Useful commands:
echo    View logs: docker-compose logs -f
echo    Stop services: docker-compose down
echo    Restart: docker-compose restart
echo    Rebuild: docker-compose up -d --build
echo.
echo 🔍 Troubleshooting:
echo    If services fail to start, check the logs:
echo    docker-compose logs [service-name]
echo.
echo Happy learning! 🧠✨
pause
