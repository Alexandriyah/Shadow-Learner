import os
import sys
import joblib
# Make sure ml module and its subfolders are in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../ml")))

from ml.recommendation import EducationalRecommender
from ml.difficulty_predictor import QuizDifficultyPredictor
from ml.progress_predictor import ProgressPredictor

class MLService:
    def __init__(self):
        self.recommender = None
        self.difficulty_predictor = None
        self.progress_predictor = None
        self.load_models()
        
    def load_models(self):
        # Paths relative to the project root (backend startup context)
        recommender_path = "ml/recommender.joblib"
        difficulty_path = "ml/difficulty_model.joblib"
        progress_path = "ml/progress_model.joblib"
        
        # Load Recommender
        if os.path.exists(recommender_path):
            try:
                self.recommender = EducationalRecommender.load(recommender_path)
                print("Loaded recommendation engine successfully.")
            except Exception as e:
                print(f"Error loading recommendation engine: {e}")
        else:
            print("Recommendation engine binary not found. Creating fallback model.")
            self.recommender = EducationalRecommender()
            self.recommender.fit()
            
        # Load Difficulty Predictor
        if os.path.exists(difficulty_path):
            try:
                self.difficulty_predictor = QuizDifficultyPredictor.load(difficulty_path)
                print("Loaded quiz difficulty predictor successfully.")
            except Exception as e:
                print(f"Error loading quiz difficulty predictor: {e}")
        else:
            print("Quiz difficulty predictor binary not found. Creating fallback model.")
            self.difficulty_predictor = QuizDifficultyPredictor()
            self.difficulty_predictor.train()
            
        # Load Progress Predictor
        if os.path.exists(progress_path):
            try:
                self.progress_predictor = ProgressPredictor.load(progress_path)
                print("Loaded student progress predictor successfully.")
            except Exception as e:
                print(f"Error loading student progress predictor: {e}")
        else:
            print("Student progress predictor binary not found. Creating fallback model.")
            self.progress_predictor = ProgressPredictor()
            self.progress_predictor.train()

    def get_recommendations(self, student_id: str, top_n: int = 5):
        if not self.recommender:
            return []
        try:
            return self.recommender.recommend_collaborative(student_id, top_n)
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return self.recommender.recommend_cold_start(top_n=top_n)

    def get_similar_topics(self, topic_name: str, top_n: int = 5):
        if not self.recommender:
            return []
        try:
            return self.recommender.recommend_content_based(topic_name, top_n)
        except Exception as e:
            print(f"Error getting content-based recommendations: {e}")
            return []

    def predict_difficulty(self, grade: int, subject: str, q_type: str, question_text: str, options_text: str) -> str:
        if not self.difficulty_predictor:
            return "Medium"
        try:
            return self.difficulty_predictor.predict(grade, subject, q_type, question_text, options_text)
        except Exception as e:
            print(f"Error predicting difficulty: {e}")
            return "Medium"

    def predict_mastery(self, quiz_score: float, completion_time: int, grade: int, topic_difficulty: str, subject: str) -> str:
        if not self.progress_predictor:
            return "Proficient"
        try:
            return self.progress_predictor.predict(quiz_score, completion_time, grade, topic_difficulty, subject)
        except Exception as e:
            print(f"Error predicting student mastery: {e}")
            # simple rule fallback
            if quiz_score >= 85:
                return "Mastered"
            elif quiz_score >= 60:
                return "Proficient"
            else:
                return "Needs Improvement"

ml_service = MLService()
