import os
from recommendation import EducationalRecommender
from difficulty_predictor import QuizDifficultyPredictor
from progress_predictor import ProgressPredictor

def main():
    print("Starting Machine Learning Model Training Pipeline...")
    
    # 1. Fit & Save Recommendation Engine
    print("\n--- Training Recommendation Engine ---")
    recommender = EducationalRecommender()
    recommender.fit()
    recommender.save("ml/recommender.joblib")
    
    # 2. Train & Save Quiz Difficulty Predictor
    print("\n--- Training Quiz Difficulty Predictor ---")
    difficulty_predictor = QuizDifficultyPredictor()
    difficulty_predictor.train()
    difficulty_predictor.save("ml/difficulty_model.joblib")
    
    # 3. Train & Save Student Progress Predictor
    print("\n--- Training Student Progress Predictor ---")
    progress_predictor = ProgressPredictor()
    progress_predictor.train()
    progress_predictor.save("ml/progress_model.joblib")
    
    print("\nAll ML models trained and saved successfully in the 'ml/' directory!")

if __name__ == "__main__":
    main()
