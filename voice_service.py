import os
import io
from typing import AsyncGenerator, Optional
import asyncio

# Initialize variables to None first
VoiceSettings = None
generate = None
voices = None
set_api_key = None
ElevenLabs = None

# Try to import ElevenLabs with proper fallback handling
try:
    from elevenlabs import VoiceSettings, generate, voices, set_api_key
except ImportError:
    try:
        # Try newer ElevenLabs API
        from elevenlabs.client import ElevenLabs
        from elevenlabs import VoiceSettings, voices, set_api_key
        generate = None  # Will need to be handled differently
    except ImportError:
        # Fallback for when ElevenLabs is not available - keep all as None
        pass

# Load API key from environment variable
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Set API key for ElevenLabs
if ELEVENLABS_API_KEY:
    set_api_key(ELEVENLABS_API_KEY)

async def transcribe_audio(audio_bytes: bytes, diarize: bool = True) -> dict:
    """
    Transcribe audio bytes to text using ElevenLabs STT.
    
    Args:
        audio_bytes: Raw audio data
        diarize: Whether to enable speaker diarization
        
    Returns:
        Dictionary with transcription and optional speaker info
    """
    if not ELEVENLABS_API_KEY:
        raise ValueError("ElevenLabs API key not configured")
    
    try:
        # Note: ElevenLabs 0.2.27 doesn't have STT in the same way
        # For now, return a mock response until we upgrade to a version with STT
        # or implement an alternative STT solution
        return {
            "text": "Mock transcription - STT not available in this ElevenLabs version",
            "speakers": None
        }
        
    except Exception as e:
        raise Exception(f"Transcription failed: {str(e)}")

async def synthesize_speech(
    text: str, 
    voice_id: str = "21m00Tcm4TlvDq8ikWAM",  # Default to Rachel voice
    model_id: str = "eleven_monolingual_v1",
    stream: bool = True
) -> AsyncGenerator[bytes, None]:
    """
    Synthesize speech from text using ElevenLabs TTS.
    
    Args:
        text: Text to synthesize
        voice_id: ElevenLabs voice ID (default: Rachel)
        model_id: TTS model to use
        stream: Whether to stream audio chunks
        
    Yields:
        Audio chunks as bytes
    """
    if not ELEVENLABS_API_KEY:
        raise ValueError("ElevenLabs API key not configured")
    
    if generate is None:
        raise ValueError("ElevenLabs generate function not available - library version mismatch")
    
    try:
        # Voice settings for natural speech
        voice_settings = VoiceSettings(
            stability=0.5,
            similarity_boost=0.8,
            style=0.0,
            use_speaker_boost=True
        )
        
        # Generate audio using the functional API
        audio_stream = generate(
            text=text,
            voice=voice_id,
            model=model_id,
            voice_settings=voice_settings,
            stream=stream
        )
        
        # Stream audio chunks
        for chunk in audio_stream:
            if chunk:
                yield chunk
                
    except Exception as e:
        raise Exception(f"Speech synthesis failed: {str(e)}")

# Helper function to get available voices
async def get_available_voices():
    """Get list of available ElevenLabs voices."""
    if not ELEVENLABS_API_KEY or voices is None:
        return []
    
    try:
        loop = asyncio.get_event_loop()
        voices_list = await loop.run_in_executor(None, voices)
        return [{"id": v.voice_id, "name": v.name} for v in voices_list]
    except:
        return []

# Voice presets for different agent personas
VOICE_PRESETS = {
    "interviewer": {
        "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel - professional, clear
        "settings": {
            "stability": 0.6,
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True
        }
    },
    "assistant": {
        "voice_id": "pNInz6obpgDQGcFmaJgB",  # Adam - friendly, approachable
        "settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.2,
            "use_speaker_boost": True
        }
    }
} 