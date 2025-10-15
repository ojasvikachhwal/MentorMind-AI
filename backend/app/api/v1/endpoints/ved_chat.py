from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import openai
import os
import google.generativeai as genai
from google.oauth2 import service_account
import json
from app.core.config import settings

router = APIRouter()

# Google Gemini configuration
if settings.GEMINI_API_KEY:
    # Use API key authentication (preferred for Gemini)
    genai.configure(api_key=settings.GEMINI_API_KEY)
elif settings.GEMINI_SERVICE_ACCOUNT_PATH:
    # Use service account authentication (fallback)
    try:
        credentials = service_account.Credentials.from_service_account_file(
            settings.GEMINI_SERVICE_ACCOUNT_PATH,
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        genai.configure(credentials=credentials)
    except Exception as e:
        print(f"Service account authentication failed: {e}")
        raise ValueError("Gemini service account authentication failed. Please use GEMINI_API_KEY instead.")
else:
    raise ValueError("GEMINI_API_KEY environment variable is required")

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')

# OpenAI configuration (fallback)
if settings.OPENAI_API_KEY:
    openai.api_key = settings.OPENAI_API_KEY

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    question: str

class ChatResponse(BaseModel):
    reply: str

@router.post("/ved-chat", response_model=ChatResponse)
async def ved_chat(request: ChatRequest):
    """
    VED AI Assistant Chat Endpoint
    Processes chat messages and returns AI responses using Google Gemini
    """
    try:
        # Prepare system prompt for VED
        system_prompt = """You are VED, an AI coding assistant and tutor. You help students with:
        - Programming concepts and theory
        - Code reviews and debugging
        - Learning new technologies
        - Problem-solving strategies
        - Best practices and optimization
        
        Be helpful, encouraging, and educational. Provide clear explanations and examples when appropriate.
        If asked about code, analyze it thoroughly and suggest improvements."""
        
        # Convert messages to Gemini format
        chat_history = []
        
        # Add system message as first user message
        chat_history.append({"role": "user", "parts": [system_prompt]})
        chat_history.append({"role": "model", "parts": ["I understand. I'm VED, your AI coding assistant. How can I help you today?"]})
        
        # Add conversation history
        for message in request.messages:
            if message.role == "user":
                chat_history.append({"role": "user", "parts": [message.content]})
            elif message.role == "assistant":
                chat_history.append({"role": "model", "parts": [message.content]})
        
        # Start a chat session with history
        chat = model.start_chat(history=chat_history)
        
        # Send the new question
        response = chat.send_message(request.question)
        
        return ChatResponse(reply=response.text)
        
    except Exception as e:
        # Fallback to OpenAI if Gemini fails
        if settings.OPENAI_API_KEY:
            try:
                # Prepare messages for OpenAI API
                openai_messages = []
                
                # Add system message to establish VED's role
                system_message = {
                    "role": "system",
                    "content": """You are VED, an AI coding assistant and tutor. You help students with:
                    - Programming concepts and theory
                    - Code reviews and debugging
                    - Learning new technologies
                    - Problem-solving strategies
                    - Best practices and optimization
                    
                    Be helpful, encouraging, and educational. Provide clear explanations and examples when appropriate.
                    If asked about code, analyze it thoroughly and suggest improvements."""
                }
                openai_messages.append(system_message)
                
                # Add conversation history
                for message in request.messages:
                    openai_messages.append({
                        "role": message.role,
                        "content": message.content
                    })
                
                # Call OpenAI API
                response = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=openai_messages,
                    max_tokens=1000,
                    temperature=0.7,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                
                # Extract the response
                ai_reply = response.choices[0].message.content
                
                return ChatResponse(reply=ai_reply)
                
            except Exception as openai_error:
                raise HTTPException(
                    status_code=500,
                    detail=f"Both Gemini and OpenAI API errors. Gemini: {str(e)}, OpenAI: {str(openai_error)}"
                )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Gemini API error: {str(e)}"
            )

@router.get("/ved-status")
async def ved_status():
    """
    Check VED service status
    """
    return {
        "status": "active",
        "service": "VED AI Assistant",
        "model": "gemini-2.0-flash",
        "version": "1.0.0",
        "gemini_configured": bool(settings.GEMINI_API_KEY or settings.GEMINI_SERVICE_ACCOUNT_PATH),
        "openai_configured": bool(settings.OPENAI_API_KEY),
        "primary_ai": "gemini" if (settings.GEMINI_API_KEY or settings.GEMINI_SERVICE_ACCOUNT_PATH) else "openai"
    }

@router.get("/test-gemini")
async def test_gemini():
    """
    Test Gemini connection
    """
    try:
        # Simple test call to Gemini
        response = model.generate_content("Hello, this is a test.")
        
        return {
            "status": "success",
            "message": "Gemini connection successful",
            "response": response.text
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Gemini connection failed: {str(e)}",
            "api_key_configured": bool(settings.GEMINI_API_KEY),
            "service_account_configured": bool(settings.GEMINI_SERVICE_ACCOUNT_PATH)
        }

@router.get("/test-openai")
async def test_openai():
    """
    Test OpenAI connection
    """
    try:
        # Simple test call to OpenAI
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Hello, this is a test."}],
            max_tokens=10
        )
        
        return {
            "status": "success",
            "message": "OpenAI connection successful",
            "response": response.choices[0].message.content
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"OpenAI connection failed: {str(e)}",
            "api_key_configured": bool(settings.OPENAI_API_KEY)
        }
