from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    grade = Column(Integer, default=5)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    progress = relationship("Progress", back_populates="user", cascade="all, delete-orphan")

class Subject(Base):
    __tablename__ = "subjects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    icon = Column(String, nullable=True) # Icon name/identifier (e.g. "Science", "Maths")
    
    topics = relationship("Topic", back_populates="subject", cascade="all, delete-orphan")

class Topic(Base):
    __tablename__ = "topics"
    
    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    name = Column(String, index=True, nullable=False)
    grade = Column(Integer, index=True, nullable=False)
    description = Column(Text, nullable=True)
    keywords = Column(String, nullable=True)
    difficulty = Column(String, nullable=True) # Easy, Medium, Hard
    
    subject = relationship("Subject", back_populates="topics")
    quizzes = relationship("Quiz", back_populates="topic", cascade="all, delete-orphan")
    flashcards = relationship("Flashcard", back_populates="topic", cascade="all, delete-orphan")

class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    options = Column(Text, nullable=True) # Pipe-separated options: "A|B|C|D"
    difficulty = Column(String, nullable=True) # Easy, Medium, Hard
    type = Column(String, nullable=True) # MCQ, True/False, Fill in the Blanks, Match the Following
    
    topic = relationship("Topic", back_populates="quizzes")

class Flashcard(Base):
    __tablename__ = "flashcards"
    
    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    front = Column(Text, nullable=False)
    back = Column(Text, nullable=False)
    
    topic = relationship("Topic", back_populates="flashcards")

class Progress(Base):
    __tablename__ = "progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    quiz_score = Column(Float, default=0.0)
    completion_time = Column(Integer, default=0) # in seconds
    mastery_level = Column(String, default="Needs Improvement") # Needs Improvement, Proficient, Mastered
    attempted_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="progress")
    topic = relationship("Topic")
