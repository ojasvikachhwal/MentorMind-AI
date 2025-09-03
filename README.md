# 🚀 MentorMind - AI-Powered Learning Platform

A comprehensive learning platform that combines adaptive quizzes, AI tutoring, and gamification to create an engaging educational experience for computer science students.

## ✨ Features

- **🔐 User Authentication**: JWT-based login/register with password reset
- **🧠 Adaptive Quiz System**: AI-powered difficulty adjustment based on performance
- **📊 Performance Dashboard**: Interactive charts showing progress and weak areas
- **🤖 AI Tutor**: Hugging Face-powered chatbot for answering study questions
- **🎯 Recommendation Engine**: ML-based suggestions for topics and resources
- **🏆 Gamification**: Leaderboards, badges, and streaks
- **🎤 Voice Interaction**: Speech-to-text for hands-free learning
- **📱 Modern UI**: Responsive Angular frontend with Bootstrap and Chart.js

## 🏗️ Architecture

```
Frontend (Angular) ←→ Backend (FastAPI) ←→ Database (PostgreSQL)
       ↓                    ↓                    ↓
   Bootstrap UI        AI/ML Modules      Redis Cache
   Chart.js           JWT Auth           Session Store
   NgRx Store         REST APIs          Performance Data
```

## 🛠️ Tech Stack

### Frontend
- **Angular 17** - Modern web framework
- **Bootstrap 5** - Responsive UI components
- **Chart.js** - Interactive data visualization
- **NgRx** - State management
- **TypeScript** - Type-safe development

### Backend
- **FastAPI** - High-performance Python web framework
- **SQLAlchemy** - Database ORM
- **PostgreSQL** - Primary database
- **Redis** - Caching and sessions
- **JWT** - Authentication

### AI/ML
- **Hugging Face** - Pre-trained language models
- **PyTorch/TensorFlow** - Deep learning frameworks
- **Scikit-learn** - Machine learning algorithms
- **spaCy** - Natural language processing
- **Google Cloud Speech** - Speech-to-text

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-service orchestration
- **GitHub Actions** - CI/CD pipeline
- **AWS** - Cloud deployment (EC2, RDS, S3)

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/mentormind.git
cd mentormind
```

### 2. Environment Setup
```bash
# Copy environment template
cp env.example .env

# Edit environment variables
nano .env
```

### 3. Start the Application
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 4. Access the Application
- **Frontend**: http://localhost:4200
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database**: localhost:5432

## 📁 Project Structure

```
mentormind/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core configuration
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── ai/             # AI/ML modules
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Backend container
├── frontend/               # Angular frontend
│   ├── src/
│   │   ├── app/           # Application components
│   │   ├── features/      # Feature modules
│   │   ├── shared/        # Shared components
│   │   └── store/         # NgRx state management
│   ├── package.json       # Node dependencies
│   └── Dockerfile         # Frontend container
├── database/               # Database scripts
│   └── init/              # Initialization scripts
├── docker-compose.yml      # Service orchestration
├── .env.example           # Environment template
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# Database
DATABASE_URL=postgresql://mentormind_user:mentormind_password@localhost:5432/mentormind

# JWT
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Google Cloud Speech-to-Text API
GOOGLE_CLOUD_CREDENTIALS=path/to/your/google-credentials.json
GOOGLE_CLOUD_PROJECT_ID=your-project-id

# Hugging Face API
HUGGINGFACE_API_KEY=your-huggingface-api-key

# Redis
REDIS_URL=redis://localhost:6379

# Frontend/Backend URLs
FRONTEND_URL=http://localhost:4200
BACKEND_URL=http://localhost:8000

# Environment
ENVIRONMENT=development
```

### AI Model Configuration

The platform uses several AI models:

1. **Hugging Face Models**: Download automatically on first use
2. **spaCy Models**: English language model
3. **Custom Models**: Stored in `ai_models/` directory

## 📚 API Documentation

### Authentication Endpoints
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/refresh-token` - Refresh access token
- `POST /auth/forgot-password` - Password reset request

### Quiz Endpoints
- `GET /quizzes/` - Get available quizzes
- `POST /quizzes/{id}/start` - Start quiz attempt
- `POST /quizzes/{id}/submit-answer` - Submit answer
- `POST /quizzes/{id}/complete` - Complete quiz

### AI Tutor Endpoints
- `POST /ai-tutor/ask` - Ask AI tutor question
- `GET /ai-tutor/topics` - Get available topics
- `POST /ai-tutor/study-recommendations` - Get recommendations

### Performance Endpoints
- `GET /performance/overview` - User performance overview
- `GET /performance/analytics` - Detailed analytics
- `GET /performance/weak-areas` - Identify weak areas

### Voice Endpoints
- `POST /voice/speech-to-text` - Convert speech to text
- `POST /voice/text-to-speech` - Convert text to speech
- `POST /voice/voice-question` - Ask question via voice

## 🧪 Testing

### Backend Testing
```bash
cd backend
pip install -r requirements.txt
pytest
```

### Frontend Testing
```bash
cd frontend
npm install
npm test
```

### E2E Testing
```bash
cd frontend
npm run e2e
```

## 🚀 Deployment

### Local Development
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Rebuild and restart
docker-compose up -d --build
```

### Production Deployment

1. **AWS Setup**
   ```bash
   # Configure AWS credentials
   aws configure
   
   # Create ECS cluster
   aws ecs create-cluster --cluster-name mentormind
   
   # Deploy to ECS
   docker-compose -f docker-compose.prod.yml up -d
   ```

2. **Environment Variables**
   - Set production environment variables
   - Configure SSL certificates
   - Set up monitoring and logging

3. **Scaling**
   ```bash
   # Scale backend services
   docker-compose up -d --scale backend=3
   
   # Scale frontend services
   docker-compose up -d --scale frontend=2
   ```

## 📊 Monitoring & Logging

### Health Checks
- Database: `pg_isready`
- Backend: `/health` endpoint
- Frontend: `/health` endpoint
- Redis: `redis-cli ping`

### Logs
```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend

# Follow logs in real-time
docker-compose logs -f
```

### Performance Monitoring
- Backend: FastAPI built-in metrics
- Database: PostgreSQL performance views
- Frontend: Angular performance monitoring

## 🔒 Security

### Authentication
- JWT tokens with configurable expiration
- Password hashing with bcrypt
- Rate limiting on API endpoints

### Data Protection
- HTTPS in production
- SQL injection prevention with SQLAlchemy
- XSS protection with Angular sanitization

### API Security
- CORS configuration
- Input validation with Pydantic
- Authentication guards on protected routes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow Angular style guide
- Use TypeScript strict mode
- Write unit tests for new features
- Update documentation for API changes

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Common Issues

1. **Database Connection Error**
   ```bash
   # Check if PostgreSQL is running
   docker-compose ps postgres
   
   # Restart database service
   docker-compose restart postgres
   ```

2. **Port Already in Use**
   ```bash
   # Check what's using the port
   lsof -i :8000
   
   # Stop conflicting services
   sudo systemctl stop conflicting-service
   ```

3. **AI Models Not Loading**
   ```bash
   # Check AI models directory
   ls -la backend/ai_models/
   
   # Rebuild backend container
   docker-compose up -d --build backend
   ```

### Getting Help
- **Issues**: Create a GitHub issue
- **Discussions**: Use GitHub Discussions
- **Documentation**: Check the `/docs` folder
- **Email**: support@mentormind.ai

## 🎯 Roadmap

### Phase 1 (Current)
- ✅ Core authentication system
- ✅ Basic quiz functionality
- ✅ AI tutor integration
- ✅ Performance tracking

### Phase 2 (Next)
- 🔄 Advanced analytics dashboard
- 🔄 Collaborative learning features
- 🔄 Mobile app development
- 🔄 Advanced AI models

### Phase 3 (Future)
- 📋 Virtual reality learning
- 📋 Advanced gamification
- 📋 Multi-language support
- 📋 Enterprise features

## 🙏 Acknowledgments

- **Hugging Face** for pre-trained language models
- **FastAPI** team for the excellent web framework
- **Angular** team for the robust frontend framework
- **OpenAI** for inspiration in AI-powered learning

---

**Made with ❤️ by the MentorMind Team**

*Empowering students to learn smarter, not harder.*
