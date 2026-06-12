import pytest
from app import models

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_user_signup_and_login(client):
    # SignUp
    signup_data = {
        "username": "learner123",
        "email": "learner@gmail.com",
        "grade": 5,
        "password": "securepassword"
    }
    response = client.post("/api/v1/auth/signup", json=signup_data)
    assert response.status_code == 200
    assert response.json()["username"] == "learner123"
    assert "id" in response.json()
    
    # Login
    login_data = {
        "username": "learner123",
        "password": "securepassword"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_subjects_and_topics(client, db_session):
    # Seed mock data
    sub = models.Subject(name="Science", icon="science")
    db_session.add(sub)
    db_session.commit()
    db_session.refresh(sub)
    
    topic = models.Topic(
        subject_id=sub.id,
        name="Photosynthesis",
        grade=5,
        description="Plants cook food",
        keywords="leaves, chloroplasts",
        difficulty="Easy"
    )
    db_session.add(topic)
    db_session.commit()
    
    # SignUp & Login
    signup_data = {"username": "kid", "email": "kid@kid.com", "grade": 5, "password": "pass"}
    client.post("/api/v1/auth/signup", json=signup_data)
    token_resp = client.post("/api/v1/auth/login", data={"username": "kid", "password": "pass"})
    token = token_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # List subjects
    resp = client.get("/api/v1/subjects", headers=headers)
    assert resp.status_code == 200
    assert len(resp.json()) >= 1
    assert resp.json()[0]["name"] == "Science"
    
    # List topics
    resp = client.get("/api/v1/subjects/Science/topics", headers=headers)
    assert resp.status_code == 200
    assert len(resp.json()) >= 1
    assert resp.json()[0]["name"] == "Photosynthesis"

def test_quiz_verification_and_logging(client, db_session):
    sub = models.Subject(name="Mathematics", icon="maths")
    db_session.add(sub)
    db_session.commit()
    
    topic = models.Topic(
        subject_id=sub.id,
        name="Fractions",
        grade=4,
        description="Fractions overview",
        keywords="numerators, denominators",
        difficulty="Easy"
    )
    db_session.add(topic)
    db_session.commit()
    
    quiz = models.Quiz(
        topic_id=topic.id,
        question="What is 1/2 of 10?",
        answer="5",
        options="2|5|8|10",
        difficulty="Easy",
        type="MCQ"
    )
    db_session.add(quiz)
    db_session.commit()
    
    # Auth
    client.post("/api/v1/auth/signup", json={"username": "tst", "email": "tst@t.com", "grade": 4, "password": "pwd"})
    token_resp = client.post("/api/v1/auth/login", data={"username": "tst", "password": "pwd"})
    token = token_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Verify MCQ answer
    resp = client.post("/api/v1/quizzes/verify", json={"quiz_id": quiz.id, "selected_answer": "5"})
    assert resp.status_code == 200
    assert resp.json()["is_correct"] is True
    
    # Log progress
    resp = client.post("/api/v1/progress/log", json={
        "topic_name": "Fractions",
        "quiz_score": 100,
        "completion_time": 90
    }, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["quiz_score"] == 100
    assert "mastery_level" in resp.json()
    
    # Fetch Dashboard
    resp = client.get("/api/v1/progress/dashboard", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["total_quizzes_taken"] == 1
    assert resp.json()["average_score"] == 100.0

def test_tutor_interaction(client):
    signup_data = {"username": "tutor_kid", "email": "tkid@t.com", "grade": 6, "password": "pwd"}
    client.post("/api/v1/auth/signup", json=signup_data)
    token_resp = client.post("/api/v1/auth/login", data={"username": "tutor_kid", "password": "pwd"})
    token = token_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Chat message
    chat_payload = {
        "topic_name": "Respiration",
        "messages": [
            {"role": "user", "content": "How do cells breathe?"}
        ]
    }
    resp = client.post("/api/v1/tutor/chat", json=chat_payload, headers=headers)
    assert resp.status_code == 200
    assert "reply" in resp.json()
