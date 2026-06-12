from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from typing import List
from app.auth import get_current_user
from app.services.ai_service import ai_service
from app import schemas, models
import base64

router = APIRouter(prefix="/tutor", tags=["tutor"])

@router.post("/chat")
def chat_with_tutor(
    payload: schemas.TutorConversation,
    current_user: models.User = Depends(get_current_user)
):
    history = [m.model_dump() for m in payload.messages[:-1]]
    new_message = payload.messages[-1].content
    
    reply = ai_service.chat_with_tutor(
        topic_name=payload.topic_name,
        message_history=history,
        new_message=new_message
    )
    return {"reply": reply}

@router.post("/ocr")
async def process_ocr_notes(
    image: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user)
):
    # Read image contents
    contents = await image.read()
    
    # In a real system, we would run pytesseract or Gemini multimodal.
    # We will simulate OCR extraction on the file by checking its size/type
    # and converting to a text description, then getting Gemini / offline content.
    mock_ocr_text = f"Class Notes on Cell Biology for Grade {current_user.grade}. The mitochondria is the powerhouse of the cell. It generates ATP energy through cellular respiration. Plant cells have chloroplasts for photosynthesis. Animal cells do not have cell walls."
    
    analysis = ai_service.extract_notes_from_image(mock_ocr_text)
    return analysis

@router.post("/voice-chat")
async def voice_chat_tutor(
    audio: UploadFile = File(...),
    topic_name: str = Form(...),
    current_user: models.User = Depends(get_current_user)
):
    # Simulates speech-to-text -> tutor response -> text-to-speech
    audio_bytes = await audio.read()
    
    # Mock Speech-to-Text translation
    user_speech_text = "Why do plants need sunlight to live?"
    
    reply = ai_service.chat_with_tutor(
        topic_name=topic_name,
        message_history=[],
        new_message=user_speech_text
    )
    
    # Mock Text-to-Speech conversion
    # In a production app, we can use gTTS or system speech engine,
    # but here we return standard audio mock/base64 so frontend play button functions.
    return {
        "user_text": user_speech_text,
        "reply_text": reply,
        "audio_base64": "" # Optional audio base64 string
    }
