import os
import csv
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.config import settings
from app.database import engine, Base, SessionLocal
from app import models
from app.routers import auth, subjects, quizzes, recommendations, tutor

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Create SQL tables
    print("Initializing Database tables...")
    Base.metadata.create_all(bind=engine)
    
    # 2. Seed database from CSV if empty
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
        
    yield
    print("Shutting down application...")

def seed_database(db: Session):
    # Check if subjects exist
    if db.query(models.Subject).count() > 0:
        print("Database already seeded.")
        return
        
    print("Seeding subjects and topics database from CSV datasets...")
    
    # Paths to datasets
    topics_csv = "datasets/topics.csv"
    quizzes_csv = "datasets/quizzes.csv"
    
    if not os.path.exists(topics_csv) or not os.path.exists(quizzes_csv):
        print("CSV dataset files not found. Seed skipped.")
        return
        
    # Seed Subjects and Topics
    subjects_cache = {} # name -> Subject db object
    topic_mapping = {} # Topic Name -> Topic db ID
    
    with open(topics_csv, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sub_name = row['Subject']
            if sub_name not in subjects_cache:
                db_sub = models.Subject(name=sub_name, icon=sub_name.lower())
                db.add(db_sub)
                db.commit()
                db.refresh(db_sub)
                subjects_cache[sub_name] = db_sub
                
            db_topic = models.Topic(
                subject_id=subjects_cache[sub_name].id,
                name=row['Topic'],
                grade=int(row['Grade']),
                description=row.get('Description', ''),
                keywords=row.get('Keywords', ''),
                difficulty=row.get('Difficulty', 'Medium')
            )
            db.add(db_topic)
            db.commit()
            db.refresh(db_topic)
            topic_mapping[row['Topic']] = db_topic.id
            
    print(f"Successfully seeded {len(subjects_cache)} subjects and {len(topic_mapping)} topics.")
    
    # Seed Quizzes
    quiz_count = 0
    with open(quizzes_csv, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            topic_name = row['Topic']
            topic_id = topic_mapping.get(topic_name)
            if not topic_id:
                continue
                
            db_quiz = models.Quiz(
                topic_id=topic_id,
                question=row['Question'],
                answer=row['Answer'],
                options=row.get('Options', ''),
                difficulty=row.get('Difficulty', 'Medium'),
                type=row.get('Type', 'MCQ')
            )
            db.add(db_quiz)
            quiz_count += 1
            if quiz_count % 1000 == 0:
                db.commit()
                
        db.commit()
        
    print(f"Successfully seeded {quiz_count} quiz questions.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for dev/testing ease
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routing
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(subjects.router, prefix=settings.API_V1_STR)
app.include_router(quizzes.router, prefix=settings.API_V1_STR)
app.include_router(recommendations.router, prefix=settings.API_V1_STR)
app.include_router(tutor.router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {"message": "Welcome to VisualLearn AI API Server!"}
