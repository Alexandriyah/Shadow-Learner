from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.auth import get_current_user
from app.services.ml_service import ml_service
from app import schemas, models

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.get("", response_model=List[schemas.TopicBase])
def get_user_recommendations(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    student_id = f"STU{str(current_user.id).zfill(4)}"
    
    # Get recommendations from ML collaborative model
    recommended_dicts = ml_service.get_recommendations(student_id=student_id, top_n=5)
    
    # Map back to schemas
    results = []
    for r in recommended_dicts:
        results.append(schemas.TopicBase(
            name=r["Topic"],
            subject=r["Subject"],
            grade=r["Grade"],
            difficulty=r["Difficulty"]
        ))
    return results
