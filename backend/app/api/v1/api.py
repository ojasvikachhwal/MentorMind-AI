from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, quizzes, performance, gamification, ai_tutor, voice, health, assessment, subjects, courses, question_analysis, admin, progress, ved_chat, mock_tests, automated_mock_tests, code_execution

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(quizzes.router, prefix="/quizzes", tags=["quizzes"])
api_router.include_router(performance.router, prefix="/performance", tags=["performance"])
api_router.include_router(gamification.router, prefix="/gamification", tags=["gamification"])
api_router.include_router(ai_tutor.router, prefix="/ai-tutor", tags=["ai-tutor"])
api_router.include_router(voice.router, prefix="/voice", tags=["voice"])
api_router.include_router(assessment.router, prefix="/assessment", tags=["assessment"])
api_router.include_router(subjects.router, tags=["subjects"])
api_router.include_router(courses.router, tags=["courses"])
api_router.include_router(question_analysis.router, tags=["question-analysis"])
api_router.include_router(progress.router, prefix="/progress", tags=["progress"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(ved_chat.router, prefix="/ved", tags=["ved-chat"])
api_router.include_router(mock_tests.router, prefix="/mock-tests", tags=["mock-tests"])
api_router.include_router(automated_mock_tests.router, prefix="/automated-tests", tags=["automated-mock-tests"])
api_router.include_router(code_execution.router, prefix="/code", tags=["code-execution"])
