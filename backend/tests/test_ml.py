import pytest
from app.services.ml_service import ml_service

def test_ml_service_recommendations():
    # Test recommendations (should work regardless of database seeding since it uses fallback models if missing binary files)
    recs = ml_service.get_recommendations(student_id="STU0001", top_n=3)
    assert isinstance(recs, list)
    assert len(recs) > 0
    assert "Topic" in recs[0]

def test_ml_service_difficulty_prediction():
    difficulty = ml_service.predict_difficulty(
        grade=5,
        subject="Science",
        q_type="MCQ",
        question_text="What happens when you mix baking soda and vinegar?",
        options_text="It bubbles.|Nothing happens.|It freezes.|It melts."
    )
    assert difficulty in ["Easy", "Medium", "Hard"]

def test_ml_service_progress_prediction():
    mastery = ml_service.predict_mastery(
        quiz_score=90.0,
        completion_time=100,
        grade=5,
        topic_difficulty="Medium",
        subject="Science"
    )
    assert mastery in ["Mastered", "Proficient", "Needs Improvement"]
