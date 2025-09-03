import os
import tempfile
from typing import Dict, Optional, Tuple
import wave
import numpy as np
from app.core.config import settings

class VoiceProcessor:
    """
    Voice processing module for speech-to-text and text-to-speech conversion
    using Google Cloud Speech API.
    """
    
    def __init__(self):
        print("🆕 Initialized simplified voice processor")
    
    def _initialize_clients(self):
        """Simplified client initialization - no Google Cloud for now."""
        print("📝 Using simplified voice processor without Google Cloud")
        pass
    
    def speech_to_text(self, audio_data: bytes, language_code: str = "en-US") -> Dict:
        """
        Simplified speech-to-text conversion (placeholder).
        
        Args:
            audio_data: Raw audio bytes
            language_code: Language code (e.g., 'en-US', 'en-GB')
        
        Returns:
            Dict containing transcription and confidence
        """
                # Placeholder implementation - returns a mock response
        return {
            "success": True,
            "transcript": "This is a placeholder transcription. Speech-to-text is not available in simplified mode.",
            "confidence": 0.8,
            "alternatives": []
        }
    
    def text_to_speech(self, text: str, voice_name: str = "en-US-Standard-A") -> Optional[bytes]:
        """
        Convert text to speech using Google Cloud Text-to-Speech API.
        
        Args:
            text: Text to convert to speech
            voice_name: Voice to use for synthesis
        
        Returns:
            Audio data as bytes, or None if failed
        """
        if not self.tts_client:
            print("⚠️ Text-to-speech client not initialized")
            return None
        
        try:
            # Configure synthesis input
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            # Configure voice
            voice = texttospeech.VoiceSelectionParams(
                language_code="en-US",
                name=voice_name,
                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
            )
            
            # Configure audio
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=0.9,
                pitch=0.0
            )
            
            # Perform synthesis
            response = self.tts_client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )
            
            return response.audio_content
            
        except Exception as e:
            print(f"❌ Text-to-speech error: {e}")
            return None
    
    def process_audio_file(self, file_path: str, language_code: str = "en-US") -> Dict:
        """
        Process an audio file for speech recognition.
        
        Args:
            file_path: Path to audio file
            language_code: Language code for recognition
        
        Returns:
            Dict containing transcription results
        """
        try:
            # Read audio file
            with open(file_path, "rb") as audio_file:
                audio_data = audio_file.read()
            
            # Convert to text
            return self.speech_to_text(audio_data, language_code)
            
        except Exception as e:
            print(f"❌ Audio file processing error: {e}")
            return {
                "success": False,
                "error": str(e),
                "transcript": "",
                "confidence": 0.0
            }
    
    def validate_audio_format(self, audio_data: bytes) -> Tuple[bool, str]:
        """
        Validate audio format and provide feedback.
        
        Args:
            audio_data: Raw audio data
        
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            # Check minimum size (1 second of audio at 16kHz, 16-bit)
            min_size = 16000 * 2  # 16kHz * 2 bytes per sample
            if len(audio_data) < min_size:
                return False, "Audio too short. Please record at least 1 second of audio."
            
            # Check maximum size (10 minutes of audio)
            max_size = 16000 * 2 * 60 * 10  # 10 minutes
            if len(audio_data) > max_size:
                return False, "Audio too long. Please keep recordings under 10 minutes."
            
            return True, "Audio format is valid"
            
        except Exception as e:
            return False, f"Error validating audio: {str(e)}"
    
    def get_supported_languages(self) -> list:
        """Get list of supported language codes."""
        return [
            "en-US", "en-GB", "en-AU", "en-CA",
            "es-ES", "es-MX", "fr-FR", "de-DE",
            "it-IT", "pt-BR", "ru-RU", "ja-JP",
            "ko-KR", "zh-CN", "hi-IN"
        ]
    
    def get_available_voices(self) -> list:
        """Get list of available voice names."""
        return [
            "en-US-Standard-A", "en-US-Standard-B", "en-US-Standard-C",
            "en-US-Standard-D", "en-US-Standard-E", "en-US-Standard-F",
            "en-US-Standard-G", "en-US-Standard-H", "en-US-Standard-I",
            "en-US-Standard-J"
        ]
    
    def create_audio_response(self, text: str, filename: str = None) -> Optional[str]:
        """
        Create an audio file from text and save it.
        
        Args:
            text: Text to convert to speech
            filename: Optional filename for the audio file
        
        Returns:
            Path to created audio file, or None if failed
        """
        audio_data = self.text_to_speech(text)
        if not audio_data:
            return None
        
        try:
            # Create temporary file if no filename provided
            if not filename:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                    temp_file.write(audio_data)
                    return temp_file.name
            else:
                # Save to specified filename
                with open(filename, "wb") as audio_file:
                    audio_file.write(audio_data)
                return filename
                
        except Exception as e:
            print(f"❌ Error saving audio file: {e}")
            return None
    
    def cleanup_audio_file(self, file_path: str):
        """Clean up temporary audio files."""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"✅ Cleaned up audio file: {file_path}")
        except Exception as e:
            print(f"⚠️ Error cleaning up audio file: {e}")
