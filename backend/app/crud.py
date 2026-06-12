from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models, schemas
from app.auth import get_password_hash

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        grade=user.grade
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_subjects(db: Session):
    return db.query(models.Subject).all()

def get_topics_by_subject(db: Session, subject_name: str, grade: int):
    subject = db.query(models.Subject).filter(models.Subject.name.ilike(subject_name)).first()
    if not subject:
        return []
    return db.query(models.Topic).filter(
        models.Topic.subject_id == subject.id,
        models.Topic.grade == grade
    ).all()

def get_topic_by_name(db: Session, topic_name: str):
    return db.query(models.Topic).filter(models.Topic.name == topic_name).first()

def get_quizzes_by_topic(db: Session, topic_id: int):
    return db.query(models.Quiz).filter(models.Quiz.topic_id == topic_id).all()

def get_quiz(db: Session, quiz_id: int):
    return db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()

def get_flashcards_by_topic(db: Session, topic_id: int):
    return db.query(models.Flashcard).filter(models.Flashcard.topic_id == topic_id).all()

def create_flashcard(db: Session, topic_id: int, front: str, back: str):
    db_fc = models.Flashcard(topic_id=topic_id, front=front, back=back)
    db.add(db_fc)
    db.commit()
    db.refresh(db_fc)
    return db_fc

def log_progress(db: Session, user_id: int, topic_id: int, score: float, completion_time: int, mastery_level: str):
    # Check if there is an existing log for this user & topic
    existing = db.query(models.Progress).filter(
        models.Progress.user_id == user_id,
        models.Progress.topic_id == topic_id
    ).first()
    
    if existing:
        # Update if the new score is higher or if we want to log the latest attempt
        existing.quiz_score = max(existing.quiz_score, score)
        existing.completion_time = completion_time
        existing.mastery_level = mastery_level
        existing.attempted_at = func.now()
        db.commit()
        db.refresh(existing)
        return existing
    else:
        db_progress = models.Progress(
            user_id=user_id,
            topic_id=topic_id,
            quiz_score=score,
            completion_time=completion_time,
            mastery_level=mastery_level
        )
        db.add(db_progress)
        db.commit()
        db.refresh(db_progress)
        return db_progress

def get_user_progress_dashboard(db: Session, user_id: int):
    attempts = db.query(models.Progress).filter(models.Progress.user_id == user_id).all()
    
    total = len(attempts)
    avg_score = sum(a.quiz_score for a in attempts) / total if total > 0 else 0.0
    
    mastered = sum(1 for a in attempts if a.mastery_level == "Mastered")
    proficient = sum(1 for a in attempts if a.mastery_level == "Proficient")
    needs_imp = sum(1 for a in attempts if a.mastery_level == "Needs Improvement")
    
    # Format recent attempts
    recent = []
    # Sort attempts by attempted_at desc
    sorted_attempts = sorted(attempts, key=lambda x: x.attempted_at, reverse=True)[:10]
    for a in sorted_attempts:
        recent.append({
            "topic_name": a.topic.name,
            "subject_name": a.topic.subject.name,
            "quiz_score": a.quiz_score,
            "completion_time": a.completion_time,
            "mastery_level": a.mastery_level,
            "attempted_at": a.attempted_at.isoformat()
        })
        
    return {
        "total_quizzes_taken": total,
        "average_score": round(avg_score, 2),
        "mastered_count": mastered,
        "proficient_count": proficient,
        "needs_improvement_count": needs_imp,
        "recent_attempts": recent
    }
