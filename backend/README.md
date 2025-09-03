# FastAPI Assessment System

A FastAPI application with PostgreSQL database and JWT authentication, featuring a comprehensive student onboarding assessment system that analyzes skills and assigns courses accordingly.

## Features

- 🔐 JWT-based authentication
- 👤 Student registration and login
- 🗄️ PostgreSQL database with SQLAlchemy ORM
- 📊 Database migrations with Alembic
- 🔒 Password hashing with bcrypt
- 🚀 FastAPI with automatic API documentation
- 📝 Comprehensive assessment system
- 🎯 Skill-based course recommendations
- 📈 Difficulty-stratified questions
- 🏆 Level mapping (beginner/intermediate/advanced)
- 🤖 **AI-powered course recommendation engine**
- 📚 **Personalized learning paths based on performance**
- 🔍 **Weakness identification and targeted course suggestions**
- 🧠 **NLP-powered question difficulty analysis & tagging**
- 🏷️ **Automatic tag extraction using spaCy and NLTK**
- 🔄 **Batch question processing with ML-ready architecture**

## Project Structure

```
backend/
│── app/
│   │── api/v1/
│   │   │── endpoints/
│   │   │   │── assessment.py    # Assessment endpoints
│   │   │   │── auth.py          # Authentication endpoints
│   │   │   │── users.py         # User management
│   │   │   │── courses.py       # Course recommendation endpoints
│   │   │   │── question_analysis.py # NLP analysis endpoints
│   │   │   └── ...
│   │   │── api.py               # API router
│   │   ├── models/
│   │   │── assessment.py        # Assessment models
│   │   │── user.py              # User model
│   │   │── __init__.py
│   │   ├── schemas/
│   │   │── assessment.py        # Assessment schemas
│   │   │── user.py              # User schemas
│   │   │── question_analysis.py # NLP analysis schemas
│   │   │── __init__.py
│   │   ├── services/
│   │   │── assessment_service.py # Assessment business logic
│   │   │── recommendation_engine.py # AI recommendation engine
│   │   │── nlp_analysis.py      # NLP analysis service
│   │   ├── core/
│   │   │── database.py          # Database configuration
│   │   │── security.py          # JWT and password utilities
│   │   └── main.py              # FastAPI application
│── alembic/                     # Database migrations
│── requirements.txt             # Python dependencies
│── alembic.ini                 # Alembic configuration
│── env.local                   # Environment variables
│── seed.py                     # Database seeding script
│── test_assessment.py          # Assessment system tests
│── test_recommendations.py     # Recommendation system tests
│── test_recommendations_pytest.py # Pytest test suite
│── test_nlp_analysis.py        # NLP analysis tests
│── test_nlp_analysis_pytest.py # NLP analysis pytest suite
│── demo_recommendations.py      # Recommendation system demo
│── demo_nlp_analysis.py        # NLP analysis demo
└── README.md                   # This file
```

## AI-Powered Course Recommendation System

The system now includes an intelligent recommendation engine that analyzes student test results and suggests personalized courses:

### 🎯 **Recommendation Logic**

- **Performance Analysis**: Analyzes test results by subject and difficulty level
- **Weakness Identification**: Identifies specific areas where students struggle
- **Level Mapping**: Maps performance to course levels (beginner/intermediate/advanced)
- **Smart Fallbacks**: Provides alternative recommendations when preferred levels aren't available

### 📊 **API Endpoints**

#### Get Course Recommendations
```http
GET /courses/recommendations/{student_id}
```

**Response Format:**
```json
{
  "subject": "Mathematics",
  "weakness": "Basic concepts, Fundamental understanding",
  "recommended_courses": [
    {"title": "Intro to Algebra", "level": "Beginner"},
    {"title": "Basic Arithmetic", "level": "Beginner"}
  ]
}
```

#### Get My Recommendations
```http
GET /courses/recommendations/me
```

#### Get ML-Powered Recommendations
```http
GET /courses/recommendations/ml/{student_id}
```

### 🔬 **Machine Learning Integration**

The system is built with scikit-learn integration for future ML enhancements:
- **Current**: Rule-based recommendation system
- **Future**: Collaborative filtering, content-based filtering, neural networks

### 🧪 **Testing**

Run the recommendation system tests:

```bash
# Basic test
python test_recommendations.py

# Pytest suite
pytest test_recommendations_pytest.py -v
```

## NLP-Powered Question Analysis System

The system now includes advanced NLP capabilities for automatic question difficulty classification and tag extraction:

### 🧠 **Question Analyzer Features**

- **Difficulty Classification**: Rule-based classification (easy/medium/hard) based on word count and content complexity
- **Tag Extraction**: Uses spaCy and NLTK to extract relevant tags from question text
- **Complexity Scoring**: Calculates overall complexity scores based on multiple indicators
- **Subject-Aware Analysis**: Context-aware tagging using subject-specific keywords
- **ML-Ready Architecture**: Designed for easy Hugging Face model integration

### 📊 **NLP Analysis API Endpoints**

#### Analyze Single Question
```http
POST /questions/analyze
```

**Request:**
```json
{
  "subject": "Mathematics",
  "text": "Solve for x: 2x + 5 = 15"
}
```

**Response:**
```json
{
  "question": "Solve for x: 2x + 5 = 15",
  "subject": "Mathematics",
  "difficulty": "easy",
  "tags": ["algebra", "equation"],
  "confidence": 0.85,
  "analysis_method": "rule_based",
  "word_count": 7,
  "complexity_score": 0.25,
  "processing_time_ms": 45.2
}
```

#### Batch Question Analysis
```http
POST /questions/analyze/batch
```

#### Upload Questions with Analysis
```http
POST /questions/upload
```

#### Search Questions by Tags/Difficulty
```http
GET /questions/search?tags=algebra&difficulty=medium
```

### 🔍 **Difficulty Classification Logic**

The system uses a sophisticated approach combining:

1. **Word Count Thresholds**:
   - Easy: ≤15 words
   - Medium: ≤30 words  
   - Hard: >30 words

2. **Content Complexity Indicators**:
   - Mathematical symbols count
   - Technical terms frequency
   - Question complexity (clauses, conjunctions)
   - Syntactic complexity (punctuation, structure)

3. **Dynamic Adjustment**: Automatically adjusts difficulty based on content complexity

### 🏷️ **Tag Extraction Process**

1. **NLP Analysis**: Uses spaCy for part-of-speech tagging and noun chunk extraction
2. **Keyword Extraction**: Identifies nouns, proper nouns, and noun phrases
3. **Subject Keywords**: Adds subject-specific relevant terms
4. **Filtering**: Removes stop words and very short tags
5. **Ranking**: Limits to top 10 most relevant tags

### 🔮 **Hugging Face Integration Ready**

The system is designed for easy ML model integration:

```python
# Current rule-based approach
analyzer = QuestionAnalyzer()

# Future ML integration
from transformers import pipeline
ml_model = pipeline("text-classification", model="your-model")
analyzer.update_model(ml_model)
```

### 🧪 **NLP Testing**

Run the NLP analysis tests:

```bash
# Basic test
python test_nlp_analysis.py

# Pytest suite
pytest test_nlp_analysis_pytest.py -v

# Demonstration
python demo_nlp_analysis.py
```

## Prerequisites

- Python 3.8+
- PostgreSQL
- pip (Python package manager)
- scikit-learn (for ML features)
- numpy (for numerical operations)
- spaCy (for NLP analysis)
- NLTK (for natural language processing)
- textblob (for additional text analysis)

## Installation

### 1. Clone the repository and navigate to backend directory

```bash
cd backend
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Database Setup

### 1. Install PostgreSQL

Download and install PostgreSQL from [postgresql.org](https://www.postgresql.org/download/)

### 2. Create database and user

Connect to PostgreSQL as the postgres user:

```bash
psql -U postgres
```

Create a new database and user:

```sql
CREATE DATABASE fastapi_db;
CREATE USER fastapi_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE fastapi_db TO fastapi_user;
\q
```

### 3. Update environment variables

Copy `env.local` to `.env` and update the database URL:

```bash
cp env.local .env
```

Edit `.env` and update the DATABASE_URL:

```
DATABASE_URL=postgresql://fastapi_user:your_password@localhost/fastapi_db
```

### 4. Run database migrations

```bash
# Initialize Alembic (first time only)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 5. Seed the database

```bash
python seed.py
```

This will create:
- 5 subjects (Data Structures & Algorithms, OOP, DBMS, OS, Web Development)
- 30 courses (6 per subject, 2 per level)
- 50 questions (10 per subject with difficulty mix)

## Running the Application

### Development mode

```bash
uvicorn app.main:app --reload
```

The application will be available at:
- API: http://localhost:8000
- Interactive API docs: http://localhost:8000/docs
- Alternative API docs: http://localhost:8000/redoc

### Production mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Assessment System

### Overview

The assessment system provides a comprehensive onboarding experience for students:

1. **Subject Selection**: Students can choose specific subjects or take all subjects
2. **Question Stratification**: Questions are stratified by difficulty (40% easy, 40% medium, 20% hard)
3. **Scoring System**: Weighted scoring based on difficulty (easy=1pt, medium=2pts, hard=3pts)
4. **Level Mapping**: 
   - ≤ 40% → beginner
   - 41–70% → intermediate
   - > 70% → advanced
5. **Course Recommendations**: Courses matched to assessed skill level

### API Endpoints

#### Authentication

- `POST /api/v1/auth/register` - Register a new student
- `POST /api/v1/auth/login` - Login and get JWT token

#### Assessment

- `GET /api/v1/assessment/subjects` - Get all available subjects
- `POST /api/v1/assessment/assessment/start` - Start a new assessment
- `POST /api/v1/assessment/assessment/{session_id}/submit` - Submit assessment answers
- `GET /api/v1/assessment/assessment/{session_id}/results` - Get assessment results
- `GET /api/v1/assessment/recommendations/latest` - Get latest recommendations

## Usage Examples

### 1. Register a new student

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "student1",
       "email": "student1@example.com",
       "password": "password123",
       "full_name": "John Doe"
     }'
```

### 2. Login and get token

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "student1",
       "password": "password123"
     }'
```

### 3. Get available subjects

```bash
curl -X GET "http://localhost:8000/api/v1/assessment/subjects"
```

### 4. Start an assessment

```bash
curl -X POST "http://localhost:8000/api/v1/assessment/assessment/start" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -d '{
       "subject_ids": [1, 2],
       "num_questions_per_subject": 10
     }'
```

### 5. Submit assessment answers

```bash
curl -X POST "http://localhost:8000/api/v1/assessment/assessment/1/submit" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -d '{
       "answers": [
         {"question_id": 1, "selected_index": 0},
         {"question_id": 2, "selected_index": 1},
         {"question_id": 3, "selected_index": 2}
       ]
     }'
```

### 6. Get assessment results

```bash
curl -X GET "http://localhost:8000/api/v1/assessment/assessment/1/results" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 7. Get latest recommendations

```bash
curl -X GET "http://localhost:8000/api/v1/assessment/recommendations/latest" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Assessment Response Format

### Assessment Start Response

```json
{
  "session_id": 1,
  "questions": [
    {
      "id": 1,
      "subject_id": 1,
      "text": "What is the time complexity of accessing an element in an array?",
      "options": ["O(1)", "O(n)", "O(log n)", "O(n²)"],
      "difficulty": "easy"
    }
  ]
}
```

### Assessment Results Response

```json
{
  "session_id": 1,
  "status": "submitted",
  "created_at": "2024-01-01T12:00:00Z",
  "results": [
    {
      "subject_id": 1,
      "subject_name": "Data Structures & Algorithms",
      "percent_correct": 75.0,
      "weighted_score": 18,
      "level": "advanced",
      "recommended_courses": [
        {
          "id": 5,
          "title": "Dynamic Programming",
          "level": "advanced",
          "description": "Advanced algorithmic techniques"
        }
      ]
    }
  ]
}
```

## Testing

### Run the assessment test suite

```bash
python test_assessment.py
```

This will test:
- Subject listing
- User registration and authentication
- Assessment start and submission
- Results retrieval and recommendations

### Manual Testing

1. Start the server: `uvicorn app.main:app --reload`
2. Open http://localhost:8000/docs
3. Use the interactive API documentation to test endpoints

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `sqlite:///./fastapi_app.db` |
| `SECRET_KEY` | JWT secret key | `your-super-secret-key-change-this-in-production` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiration time | `30` |
| `ENVIRONMENT` | Application environment | `development` |

## Business Rules

### Question Stratification
- **Easy questions**: 40% of total questions
- **Medium questions**: 40% of total questions  
- **Hard questions**: 20% of total questions

### Scoring System
- **Easy questions**: 1 point if correct
- **Medium questions**: 2 points if correct
- **Hard questions**: 3 points if correct

### Level Mapping
- **≤ 40% correct**: Beginner level
- **41–70% correct**: Intermediate level
- **> 70% correct**: Advanced level

### Course Recommendations
1. First try to match courses at the assessed level
2. If no courses at that level, try the closest level
3. If still no courses, recommend any available courses for the subject

## Security Notes

⚠️ **Important Security Considerations:**

1. **Change the SECRET_KEY**: Update the SECRET_KEY in your `.env` file with a strong, random key
2. **Use HTTPS in production**: Always use HTTPS in production environments
3. **Database security**: Use strong passwords and limit database access
4. **Environment variables**: Never commit sensitive information to version control
5. **Input validation**: All user inputs are validated using Pydantic schemas
6. **Authentication**: All assessment endpoints require valid JWT tokens

## Development

### Adding new subjects

1. Add the subject to the seed script
2. Create corresponding courses and questions
3. Run `python seed.py` to add to database

### Adding new questions

1. Add questions to the seed script with proper difficulty distribution
2. Ensure questions have 4 options and correct_index is 0-3
3. Run `python seed.py` to add to database

### Database migrations

1. Make changes to models
2. Create migration: `alembic revision --autogenerate -m "Description"`
3. Apply migration: `alembic upgrade head`

## Troubleshooting

### Common Issues

1. **Database connection error**: Make sure PostgreSQL is running and connection string is correct
2. **Import errors**: Make sure you're in the correct directory and virtual environment is activated
3. **Migration errors**: Check that the database exists and user has proper permissions
4. **Assessment errors**: Ensure database is seeded with subjects, courses, and questions

### Getting Help

- Check the FastAPI documentation: https://fastapi.tiangolo.com/
- Check the SQLAlchemy documentation: https://docs.sqlalchemy.org/
- Check the Alembic documentation: https://alembic.sqlalchemy.org/

## License

This project is open source and available under the [MIT License](LICENSE).
