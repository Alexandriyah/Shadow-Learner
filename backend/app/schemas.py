from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    grade: int = 5

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class SubjectBase(BaseModel):
    name: str
    icon: Optional[str] = None

class SubjectResponse(SubjectBase):
    id: int
    
    class Config:
        from_attributes = True

class TopicBase(BaseModel):
    name: str
    grade: int
    description: Optional[str] = None
    keywords: Optional[str] = None
    difficulty: Optional[str] = None

class TopicResponse(TopicBase):
    id: int
    subject_id: int
    
    class Config:
        from_attributes = True

class QuizBase(BaseModel):
    question: str
    options: Optional[str] = None
    difficulty: Optional[str] = None
    type: Optional[str] = None

class QuizResponse(QuizBase):
    id: int
    topic_id: int
    
    class Config:
        from_attributes = True

class QuizVerify(BaseModel):
    quiz_id: int
    selected_answer: str

class QuizVerifyResult(BaseModel):
    quiz_id: int
    is_correct: bool
    correct_answer: str
    explanation: str

class FlashcardBase(BaseModel):
    front: str
    back: str

class FlashcardResponse(FlashcardBase):
    id: int
    topic_id: int
    
    class Config:
        from_attributes = True

class ProgressBase(BaseModel):
    topic_id: int
    quiz_score: float
    completion_time: int # in seconds

class ProgressLog(BaseModel):
    topic_name: str
    quiz_score: float
    completion_time: int

class ProgressResponse(BaseModel):
    id: int
    user_id: int
    topic_id: int
    quiz_score: float
    completion_time: int
    mastery_level: str
    attempted_at: datetime
    
    class Config:
        from_attributes = True

class ProgressDashboardInfo(BaseModel):
    total_quizzes_taken: int
    average_score: float
    mastered_count: int
    proficient_count: int
    needs_improvement_count: int
    recent_attempts: List[dict]
    
    class Config:
        from_attributes = True

class TutorMessage(BaseModel):
    role: str # user or assistant
    content: str
    voice: Optional[bool] = False

class TutorConversation(BaseModel):
    topic_name: str
    messages: List[TutorMessage]
