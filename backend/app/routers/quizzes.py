from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.auth import get_current_user
from app.services.ai_service import ai_service
from app.services.ml_service import ml_service
from app import crud, schemas, models

router = APIRouter(tags=["quizzes"])

@router.get("/topics/{topic_id}/quizzes", response_model=List[schemas.QuizResponse])
def get_topic_quizzes(topic_id: int, db: Session = Depends(get_db)):
    topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
        
    quizzes = crud.get_quizzes_by_topic(db, topic_id)
    if not quizzes:
        # Generate dynamically using AI Service
        ai_quizzes = ai_service.generate_quiz_questions(
            topic_name=topic.name,
            subject=topic.subject.name,
            grade=topic.grade
        )
        
        for q in ai_quizzes:
            db_q = models.Quiz(
                topic_id=topic_id,
                question=q["question"],
                options=q.get("options", ""),
                answer=q["answer"],
                difficulty=q.get("difficulty", "Medium"),
                type=q.get("type", "MCQ")
            )
            db.add(db_q)
        db.commit()
        quizzes = crud.get_quizzes_by_topic(db, topic_id)
        
    return quizzes

@router.get("/topics/{topic_id}/flashcards", response_model=List[schemas.FlashcardResponse])
def get_topic_flashcards(topic_id: int, db: Session = Depends(get_db)):
    topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
        
    flashcards = crud.get_flashcards_by_topic(db, topic_id)
    if not flashcards:
        # Load topic content which pre-populates flashcards
        content = ai_service.generate_topic_content(topic.name, topic.subject.name, topic.grade)
        flashcards = crud.get_flashcards_by_topic(db, topic_id)
        
    return flashcards

@router.post("/quizzes/verify", response_model=schemas.QuizVerifyResult)
def verify_quiz_answer(payload: schemas.QuizVerify, db: Session = Depends(get_db)):
    quiz = crud.get_quiz(db, payload.quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz question not found")
        
    is_correct = (payload.selected_answer.strip().lower() == quiz.answer.strip().lower())
    
    # Generate simple explanation based on correctness
    if is_correct:
        explanation = f"Spot on! '{quiz.answer}' is the correct answer. Fantastic work!"
    else:
        explanation = f"Nice try! The correct answer is '{quiz.answer}'. Keep learning and you will get it next time!"
        
    return {
        "quiz_id": quiz.id,
        "is_correct": is_correct,
        "correct_answer": quiz.answer,
        "explanation": explanation
    }

@router.post("/quizzes/predict-difficulty")
def predict_difficulty(
    grade: int,
    subject: str,
    q_type: str,
    question_text: str,
    options_text: str
):
    difficulty = ml_service.predict_difficulty(
        grade=grade,
        subject=subject,
        q_type=q_type,
        question_text=question_text,
        options_text=options_text
    )
    return {"predicted_difficulty": difficulty}

@router.post("/progress/log", response_model=schemas.ProgressResponse)
def log_student_progress(
    payload: schemas.ProgressLog,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    topic = crud.get_topic_by_name(db, topic_name=payload.topic_name)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
        
    # Use ML model to classify mastery level
    mastery = ml_service.predict_mastery(
        quiz_score=payload.quiz_score,
        completion_time=payload.completion_time,
        grade=topic.grade,
        topic_difficulty=topic.difficulty or "Medium",
        subject=topic.subject.name
    )
    
    progress_record = crud.log_progress(
        db=db,
        user_id=current_user.id,
        topic_id=topic.id,
        score=payload.quiz_score,
        completion_time=payload.completion_time,
        mastery_level=mastery
    )
    return progress_record

@router.get("/progress/dashboard", response_model=schemas.ProgressDashboardInfo)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_user_progress_dashboard(db, user_id=current_user.id)
