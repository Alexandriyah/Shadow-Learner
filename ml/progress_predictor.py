import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib

class ProgressPredictor:
    def __init__(self):
        self.model = None
        self.label_encoder = LabelEncoder()
        
    def prepare_data(self, progress_path="datasets/progress.csv", topics_path="datasets/topics.csv"):
        progress = pd.read_csv(progress_path)
        topics = pd.read_csv(topics_path)
        
        # Merge to get subject, grade, topic difficulty
        df = pd.merge(progress, topics[['Topic', 'Subject', 'Grade', 'Difficulty']], on='Topic', how='left')
        
        # Clean null values if any
        df['Grade'] = df['Grade'].fillna(5)
        df['Difficulty'] = df['Difficulty'].fillna('Medium')
        df['Subject'] = df['Subject'].fillna('Science')
        
        X = df[['Quiz_Score', 'Completion_Time', 'Grade', 'Difficulty', 'Subject']]
        y = df['Mastery_Level']
        
        y_encoded = self.label_encoder.fit_transform(y)
        
        return X, y_encoded
        
    def train(self, progress_path="datasets/progress.csv", topics_path="datasets/topics.csv"):
        X, y = self.prepare_data(progress_path, topics_path)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Preprocessing
        categorical_features = ['Difficulty', 'Subject']
        categorical_transformer = OneHotEncoder(handle_unknown='ignore')
        
        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', categorical_transformer, categorical_features)
            ],
            remainder='passthrough'
        )
        
        # Full pipeline
        self.model = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
        ])
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        report = classification_report(y_test, y_pred, target_names=self.label_encoder.classes_)
        print("Progress Predictor Mastery Level Training Report:")
        print(report)
        
    def predict(self, quiz_score, completion_time, grade, topic_difficulty, subject):
        if self.model is None:
            raise ValueError("Model is not trained yet.")
            
        input_df = pd.DataFrame([{
            'Quiz_Score': quiz_score,
            'Completion_Time': completion_time,
            'Grade': grade,
            'Difficulty': topic_difficulty,
            'Subject': subject
        }])
        
        pred_encoded = self.model.predict(input_df)[0]
        return self.label_encoder.inverse_transform([pred_encoded])[0]
        
    def save(self, file_path="ml/progress_model.joblib"):
        joblib.dump({
            'model': self.model,
            'label_encoder': self.label_encoder
        }, file_path)
        print(f"Saved progress predictor to {file_path}")
        
    @classmethod
    def load(cls, file_path="ml/progress_model.joblib"):
        data = joblib.load(file_path)
        predictor = cls()
        predictor.model = data['model']
        predictor.label_encoder = data['label_encoder']
        return predictor
