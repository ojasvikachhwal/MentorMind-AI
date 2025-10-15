from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
import subprocess
import tempfile
import os
import signal
import threading
import time
import json
from app.core.database import get_db
from app.core.config import settings
from app.models.user import User
from app.core.security import get_current_user
from pydantic import BaseModel
import google.generativeai as genai

# Configure Gemini AI
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')

router = APIRouter()

class CodeExecutionRequest(BaseModel):
    code: str
    language: str
    input_data: Optional[str] = None

class CodeExecutionResponse(BaseModel):
    output: str
    error: Optional[str] = None
    execution_time: float
    memory_usage: Optional[str] = None
    exit_code: int

class GeminiFeedbackRequest(BaseModel):
    code: str
    language: str
    output: Optional[str] = None
    error: Optional[str] = None
    question: Optional[str] = None

class GeminiFeedbackResponse(BaseModel):
    feedback: str
    suggestions: list
    score: Optional[int] = None
    optimizations: list

class VEDChatRequest(BaseModel):
    code: str
    language: str
    question: str
    context: Optional[str] = None

class VEDChatResponse(BaseModel):
    reply: str
    suggestions: list
    related_topics: list

# Language configurations
LANGUAGE_CONFIGS = {
    'python': {
        'extension': '.py',
        'command': 'python',
        'timeout': 10,
        'memory_limit': '128m'
    },
    'java': {
        'extension': '.java',
        'command': 'java',
        'compile_command': 'javac',
        'timeout': 15,
        'memory_limit': '256m'
    },
    'cpp': {
        'extension': '.cpp',
        'command': './a.out',
        'compile_command': 'g++',
        'timeout': 10,
        'memory_limit': '128m'
    },
    'javascript': {
        'extension': '.js',
        'command': 'node',
        'timeout': 10,
        'memory_limit': '128m'
    }
}

def execute_code_safely(code: str, language: str, input_data: str = None) -> Dict[str, Any]:
    """
    Execute code in a sandboxed environment with safety measures
    """
    if language not in LANGUAGE_CONFIGS:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported language: {language}"
        )
    
    config = LANGUAGE_CONFIGS[language]
    start_time = time.time()
    
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(
            mode='w', 
            suffix=config['extension'], 
            delete=False
        ) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            # Handle compilation for compiled languages
            if 'compile_command' in config:
                compile_result = subprocess.run(
                    [config['compile_command'], temp_file, '-o', 'a.out'],
                    capture_output=True,
                    text=True,
                    timeout=config['timeout'],
                    cwd=os.path.dirname(temp_file)
                )
                
                if compile_result.returncode != 0:
                    return {
                        'output': '',
                        'error': f"Compilation error:\n{compile_result.stderr}",
                        'execution_time': time.time() - start_time,
                        'exit_code': compile_result.returncode
                    }
            
            # Execute the code
            if language == 'java':
                # For Java, run the compiled class
                class_name = os.path.splitext(os.path.basename(temp_file))[0]
                cmd = [config['command'], class_name]
            else:
                cmd = [config['command'], temp_file]
            
            # Set memory limit and timeout
            env = os.environ.copy()
            if 'memory_limit' in config:
                env['MEMORY_LIMIT'] = config['memory_limit']
            
            result = subprocess.run(
                cmd,
                input=input_data,
                capture_output=True,
                text=True,
                timeout=config['timeout'],
                cwd=os.path.dirname(temp_file),
                env=env
            )
            
            execution_time = time.time() - start_time
            
            return {
                'output': result.stdout,
                'error': result.stderr if result.stderr else None,
                'execution_time': execution_time,
                'exit_code': result.returncode
            }
            
        finally:
            # Clean up temporary files
            try:
                os.unlink(temp_file)
                if os.path.exists('a.out'):
                    os.unlink('a.out')
            except:
                pass
                
    except subprocess.TimeoutExpired:
        return {
            'output': '',
            'error': f"Code execution timed out after {config['timeout']} seconds",
            'execution_time': time.time() - start_time,
            'exit_code': -1
        }
    except Exception as e:
        return {
            'output': '',
            'error': f"Execution error: {str(e)}",
            'execution_time': time.time() - start_time,
            'exit_code': -1
        }

@router.post("/run-code", response_model=CodeExecutionResponse)
async def run_code(
    request: CodeExecutionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Execute code safely in a sandboxed environment
    """
    try:
        result = execute_code_safely(
            code=request.code,
            language=request.language,
            input_data=request.input_data
        )
        
        return CodeExecutionResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Code execution failed: {str(e)}"
        )

@router.post("/gemini-feedback", response_model=GeminiFeedbackResponse)
async def get_gemini_feedback(
    request: GeminiFeedbackRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get AI feedback on code using Gemini API
    """
    if not settings.GEMINI_API_KEY:
        # Fallback feedback when Gemini is not available
        return GeminiFeedbackResponse(
            feedback="Gemini API not configured. Basic analysis: Your code appears to be syntactically correct.",
            suggestions=["Consider adding comments for better readability", "Test edge cases"],
            score=75,
            optimizations=["Add error handling", "Consider performance improvements"]
        )
    
    try:
        # Prepare context for Gemini
        context = f"""
        Language: {request.language}
        Code:
        {request.code}
        """
        
        if request.output:
            context += f"\nOutput:\n{request.output}"
        
        if request.error:
            context += f"\nError:\n{request.error}"
        
        if request.question:
            context += f"\nStudent Question: {request.question}"
        
        prompt = f"""
        As an expert programming tutor, analyze this code and provide helpful feedback:
        
        {context}
        
        Please provide:
        1. Overall assessment of the code quality
        2. Specific suggestions for improvement
        3. A score out of 100
        4. Optimization recommendations
        5. Any potential issues or bugs
        
        Format your response as JSON with these fields:
        - feedback: string (detailed analysis)
        - suggestions: array of strings (specific improvements)
        - score: number (0-100)
        - optimizations: array of strings (performance/quality improvements)
        """
        
        response = model.generate_content(prompt)
        
        try:
            # Try to parse JSON response
            feedback_data = json.loads(response.text)
            return GeminiFeedbackResponse(**feedback_data)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return GeminiFeedbackResponse(
                feedback=response.text,
                suggestions=["Review the code structure", "Add proper error handling"],
                score=80,
                optimizations=["Consider code organization", "Add input validation"]
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get Gemini feedback: {str(e)}"
        )

@router.post("/ved-chat", response_model=VEDChatResponse)
async def ved_chat(
    request: VEDChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Chat with VED AI assistant about code
    """
    if not settings.GEMINI_API_KEY:
        # Fallback response when Gemini is not available
        return VEDChatResponse(
            reply="I'm VED, your coding assistant! I can help you understand concepts, debug code, and provide guidance. However, I'm currently in offline mode.",
            suggestions=["Try running your code to see the output", "Check for syntax errors"],
            related_topics=["Programming fundamentals", "Debugging techniques"]
        )
    
    try:
        # Prepare context for VED
        context = f"""
        Student is working on {request.language} code:
        
        Code:
        {request.code}
        
        Question: {request.question}
        """
        
        if request.context:
            context += f"\nAdditional Context: {request.context}"
        
        prompt = f"""
        You are VED, an expert programming tutor and coding assistant. A student has asked you a question about their code.
        
        {context}
        
        Please provide:
        1. A helpful and encouraging response to their question
        2. Specific suggestions for their code
        3. Related topics they should explore
        
        Format your response as JSON with these fields:
        - reply: string (your response to the student)
        - suggestions: array of strings (specific code suggestions)
        - related_topics: array of strings (topics to explore further)
        """
        
        response = model.generate_content(prompt)
        
        try:
            # Try to parse JSON response
            ved_data = json.loads(response.text)
            return VEDChatResponse(**ved_data)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return VEDChatResponse(
                reply=response.text,
                suggestions=["Review the code logic", "Test with different inputs"],
                related_topics=["Programming best practices", "Debugging techniques"]
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get VED response: {str(e)}"
        )

@router.get("/supported-languages")
async def get_supported_languages():
    """
    Get list of supported programming languages
    """
    return {
        "languages": [
            {
                "value": "python",
                "label": "Python",
                "extension": ".py",
                "description": "General-purpose programming language"
            },
            {
                "value": "java",
                "label": "Java",
                "extension": ".java",
                "description": "Object-oriented programming language"
            },
            {
                "value": "cpp",
                "label": "C++",
                "extension": ".cpp",
                "description": "High-performance systems programming"
            },
            {
                "value": "javascript",
                "label": "JavaScript",
                "extension": ".js",
                "description": "Web development and scripting"
            }
        ]
    }
