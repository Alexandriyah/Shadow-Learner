from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.auth import get_current_user
from app.services.ai_service import ai_service
from app import crud, schemas, models

router = APIRouter(tags=["subjects"])

@router.get("/subjects", response_model=List[schemas.SubjectResponse])
def read_subjects(db: Session = Depends(get_db)):
    return crud.get_subjects(db)

@router.get("/subjects/{subject_name}/topics", response_model=List[schemas.TopicResponse])
def read_topics(
    subject_name: str, 
    grade: Optional[int] = None, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    selected_grade = grade if grade is not None else current_user.grade
    topics = crud.get_topics_by_subject(db, subject_name=subject_name, grade=selected_grade)
    return topics

@router.get("/topics/{topic_id}", response_model=schemas.TopicResponse)
def read_topic(topic_id: int, db: Session = Depends(get_db)):
    topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

@router.get("/topics/{topic_id}/content")
def get_topic_content(topic_id: int, db: Session = Depends(get_db)):
    topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    # Generate full child-friendly explanations and diagrams using AI Service
    content = ai_service.generate_topic_content(
        topic_name=topic.name,
        subject=topic.subject.name,
        grade=topic.grade
    )
    
    # Pre-populate flashcards in DB if they aren't there yet
    existing_fc = crud.get_flashcards_by_topic(db, topic_id)
    if not existing_fc and "flashcards" in content:
        for card in content["flashcards"]:
            crud.create_flashcard(db, topic_id, card["front"], card["back"])
            
    return content
