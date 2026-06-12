import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib

class EducationalRecommender:
    def __init__(self, topics_path="datasets/topics.csv", progress_path="datasets/progress.csv"):
        self.topics_path = topics_path
        self.progress_path = progress_path
        self.topics_df = None
        self.progress_df = None
        self.tfidf_matrix = None
        self.tfidf_vectorizer = None
        self.student_topic_matrix = None
        self.student_similarity_df = None
        self.load_data()
        
    def load_data(self):
        if os.path.exists(self.topics_path):
            self.topics_df = pd.read_csv(self.topics_path)
        if os.path.exists(self.progress_path):
            self.progress_df = pd.read_csv(self.progress_path)
            
    def fit(self):
        if self.topics_df is None or len(self.topics_df) == 0:
            return
            
        # Fit content-based recommender
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        # Combine Topic, Description, Keywords
        combined_features = self.topics_df['Topic'] + " " + self.topics_df['Description'] + " " + self.topics_df['Keywords']
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(combined_features)
        
        # Fit collaborative filtering recommender
        if self.progress_df is not None and len(self.progress_df) > 0:
            # Create pivot table
            self.student_topic_matrix = self.progress_df.pivot_table(
                index='Student_ID', 
                columns='Topic', 
                values='Quiz_Score', 
                fill_value=0
            )
            # Compute cosine similarity between students
            if len(self.student_topic_matrix) > 1:
                student_sim = cosine_similarity(self.student_topic_matrix)
                self.student_similarity_df = pd.DataFrame(
                    student_sim, 
                    index=self.student_topic_matrix.index, 
                    columns=self.student_topic_matrix.index
                )
                
    def recommend_content_based(self, topic_name, top_n=5):
        if self.topics_df is None or self.tfidf_matrix is None:
            return []
            
        # Get index of the topic
        idx_list = self.topics_df.index[self.topics_df['Topic'] == topic_name].tolist()
        if not idx_list:
            return []
        idx = idx_list[0]
        
        # Compute cosine similarity of this topic with all other topics
        sim_scores = cosine_similarity(self.tfidf_matrix[idx], self.tfidf_matrix).flatten()
        
        # Get indices of top similar topics (excluding the queried topic itself)
        similar_indices = sim_scores.argsort()[-(top_n+1):-1][::-1]
        
        recommendations = self.topics_df.iloc[similar_indices][['Topic', 'Subject', 'Grade', 'Difficulty']].to_dict(orient='records')
        return recommendations
        
    def recommend_collaborative(self, student_id, top_n=5):
        # Cold start check: if student doesn't exist or not enough records, fall back to grade/popular recommendations
        if (self.progress_df is None or 
            self.student_topic_matrix is None or 
            student_id not in self.student_topic_matrix.index or
            self.student_similarity_df is None):
            return self.recommend_cold_start(student_id, top_n)
            
        # Find similar students
        similar_students = self.student_similarity_df[student_id].sort_values(ascending=False)
        # Exclude self
        similar_students = similar_students.drop(student_id)
        
        # Get topics completed by self
        self_records = self.progress_df[self.progress_df['Student_ID'] == student_id]
        completed_topics = set(self_records['Topic'].tolist())
        
        # Aggregate scores from similar students
        # Top 10 similar students
        top_sim_students = similar_students.head(10).index
        similar_students_progress = self.progress_df[self.progress_df['Student_ID'].isin(top_sim_students)]
        
        # Filter out already completed topics
        recommendation_candidates = similar_students_progress[~similar_students_progress['Topic'].isin(completed_topics)]
        
        if len(recommendation_candidates) == 0:
            return self.recommend_cold_start(student_id, top_n)
            
        # Group candidates by Topic and calculate mean score weighted by similarity if possible, or simple average
        grouped = recommendation_candidates.groupby('Topic').agg({'Quiz_Score': 'mean'}).reset_index()
        grouped = grouped.sort_values(by='Quiz_Score', ascending=False)
        
        top_topics = grouped.head(top_n)['Topic'].tolist()
        
        # Join with topics database to get metadata
        recommended_topics = self.topics_df[self.topics_df['Topic'].isin(top_topics)][['Topic', 'Subject', 'Grade', 'Difficulty']].to_dict(orient='records')
        return recommended_topics
        
    def recommend_cold_start(self, student_id=None, top_n=5):
        # Default cold start: return popular topics from a default grade (e.g. Grade 5)
        # or topics with high average scores
        if self.topics_df is None:
            return []
        
        # Just grab random popular ones or top 5 topics from different subjects
        unique_subjects = self.topics_df['Subject'].unique()
        selected_topics = []
        for sub in unique_subjects[:top_n]:
            sub_topics = self.topics_df[self.topics_df['Subject'] == sub]
            if len(sub_topics) > 0:
                selected_topics.append(sub_topics.iloc[0])
                
        df_selected = pd.DataFrame(selected_topics)
        return df_selected[['Topic', 'Subject', 'Grade', 'Difficulty']].to_dict(orient='records')

    def save(self, file_path="ml/recommender.joblib"):
        joblib.dump(self, file_path)
        print(f"Saved recommender model to {file_path}")
        
    @staticmethod
    def load(file_path="ml/recommender.joblib"):
        return joblib.load(file_path)
