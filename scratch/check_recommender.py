import os
import sys
import joblib

# Make sure ml module is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ml.recommendation import EducationalRecommender

print("Current Working Directory:", os.getcwd())
recommender_path = "ml/recommender.joblib"
print("File exists:", os.path.exists(recommender_path))

if os.path.exists(recommender_path):
    try:
        rec = EducationalRecommender.load(recommender_path)
        print("Recommender loaded successfully.")
        print("topics_df is None?", rec.topics_df is None)
        if rec.topics_df is not None:
            print("topics_df shape:", rec.topics_df.shape)
            recs = rec.recommend_cold_start(top_n=3)
            print("Cold start recs:", recs)
            recs_coll = rec.recommend_collaborative(student_id="STU0001", top_n=3)
            print("Collaborative recs:", recs_coll)
    except Exception as e:
        print("Error:", e)
else:
    print("Not found.")
