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

class QuizDifficultyPredictor:
    def __init__(self):
        self.model = None
        self.label_encoder = LabelEncoder()
        
    def prepare_data(self, quizzes_path="datasets/quizzes.csv", topics_path="datasets/topics.csv"):
        quizzes = pd.read_csv(quizzes_path)
        topics = pd.read_csv(topics_path)
        
        # Merge to get subject and grade
        df = pd.merge(quizzes, topicsByTopic := topics[['Topic', 'Subject', 'Grade']], on='Topic', how='left')
        
        # Feature engineering
        df['question_len'] = df['Question'].apply(lambda x: len(str(x)))
        df['word_count'] = df['Question'].apply(lambda x: len(str(x).split()))
        df['num_options'] = df['Options'].apply(lambda x: len(str(x).split('|')) if pd.notnull(x) and str(x) != "" else 0)
        
        # Clean null values if any
        df['Grade'] = df['Grade'].fillna(5)
        df['Subject'] = df['Subject'].fillna('Science')
        df['Type'] = df['Type'].fillna('MCQ')
        
        X = df[['Grade', 'Subject', 'Type', 'question_len', 'word_count', 'num_options']]
        y = df['Difficulty']
        
        # Fit label encoder for target
        y_encoded = self.label_encoder.fit_transform(y)
        
        return X, y_encoded
        
    def train(self, quizzes_path="datasets/quizzes.csv", topics_path="datasets/topics.csv"):
        X, y = self.prepare_data(quizzes_path, topics_path)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Build Preprocessing pipeline
        categorical_features = ['Subject', 'Type']
        categorical_transformer = OneHotEncoder(handle_unknown='ignore')
        
        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', categorical_transformer, categorical_features)
            ],
            remainder='passthrough'
        )
        
        # Define the full pipeline
        self.model = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
        ])
        
        # Train
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        report = classification_report(y_test, y_pred, target_names=self.label_encoder.classes_)
        print("Quiz Difficulty Predictor Training Report:")
        print(report)
        
    def predict(self, grade, subject, q_type, question_text, options_text):
        if self.model is None:
            raise ValueError("Model is not trained yet.")
            
        # Feature extraction
        question_len = len(question_text)
        word_count = len(question_text.split())
        num_options = len(options_text.split('|')) if options_text else 0
        
        input_df = pd.DataFrame([{
            'Grade': grade,
            'Subject': subject,
            'Type': q_type,
            'question_len': question_len,
            'word_count': word_count,
            'num_options': num_options
        }])
        
        pred_encoded = self.model.predict(input_df)[0]
        return self.label_encoder.inverse_transform([pred_encoded])[0]
        
    def save(self, file_path="ml/difficulty_model.joblib"):
        joblib.dump({
            'model': self.model,
            'label_encoder': self.label_encoder
        }, file_path)
        print(f"Saved difficulty predictor to {file_path}")
        
    @classmethod
    def load(cls, file_path="ml/difficulty_model.joblib"):
        data = joblib.load(file_path)
        predictor = cls()
        predictor.model = data['model']
        predictor.label_encoder = data['label_encoder']
        return predictor
