import os
import csv
import random
import pandas as pd
import numpy as np

def make_dirs():
    os.makedirs("datasets", exist_ok=True)
    os.makedirs("ml", exist_ok=True)
    os.makedirs("notebooks", exist_ok=True)
    os.makedirs("backend/app", exist_ok=True)
    os.makedirs("frontend/src", exist_ok=True)

def generate_topics():
    subjects = {
        "Science": ["Light", "Sound", "Electricity", "Magnets", "Heat", "Force", "Motion", "Simple Machines", "Adaptations", "States of Matter", "Water Cycle", "Solar System"],
        "Mathematics": ["Fractions", "Decimals", "Percentages", "Algebra", "Geometry", "Integers", "Profit and Loss", "Ratio", "Probability", "Data Handling", "Number Systems", "Measurement"],
        "Social Science": ["Ancient Civilizations", "Freedom Struggle", "Democracy", "Constitution", "Local Government", "Globe and Maps", "Weather", "Resources", "Human Rights", "Civics"],
        "English": ["Nouns", "Verbs", "Adjectives", "Pronouns", "Tenses", "Direct and Indirect Speech", "Active and Passive Voice", "Conjunctions", "Prepositions", "Subject-Verb Agreement", "Vocabulary", "Punctuation"],
        "Biology": ["Photosynthesis", "Digestion", "Respiration", "Circulation", "Nervous System", "Plant Reproduction", "Ecosystems", "Genetics", "Cell Division", "Classification of Organisms", "Microorganisms", "Health and Diseases"],
        "Physics": ["Laws of Motion", "Work and Energy", "Gravitation", "Electrostatics", "Magnetism", "Sound Waves", "Light Reflection", "Light Refraction", "Thermodynamics", "Electromagnetism", "Pressure", "Friction"],
        "Chemistry": ["Acids and Bases", "Chemical Reactions", "Periodic Table", "Atoms and Molecules", "Solutions", "Metals and Non-Metals", "Carbon Compounds", "Chemical Bonding", "States of Matter", "Coal and Petroleum", "Synthetic Fibres", "Combustion"],
        "History": ["Indus Valley Civilization", "Roman Empire", "French Revolution", "World War I", "World War II", "Industrial Revolution", "Medieval Period", "Renaissance", "American Independence", "Indian Independence", "Ancient Egypt", "Cold War"],
        "Geography": ["Solar System", "Earth's Layers", "Plate Tectonics", "Climate Zones", "Oceans", "Rivers", "Mountains", "Agriculture", "Mineral Resources", "Population Geography", "Natural Vegetation", "Maps and Scales"]
    }

    topics_list = []
    # We want 1000+ topics.
    # 9 subjects, 10 grades. For each combination, we generate 12 topics.
    # 9 * 10 * 12 = 1080 topics.
    topic_id_counter = 1
    
    for subject, base_topics in subjects.items():
        for grade in range(1, 11):
            for i in range(12):
                base = base_topics[i % len(base_topics)]
                
                # Create variations based on grade and index
                if grade <= 3:
                    prefix = "Introduction to"
                    difficulty = "Easy"
                elif grade <= 7:
                    prefix = "Understanding"
                    difficulty = "Medium"
                else:
                    prefix = "Advanced Concepts of"
                    difficulty = "Hard"
                
                suffixes = ["Basics", "Principles", "Applications", "Theories", "Exploration", "Processes", "Systems", "Impact", "Dynamics", "Functions", "Structure", "Key Ideas"]
                suffix = suffixes[i % len(suffixes)]
                
                topic_name = f"{prefix} {base} ({suffix})"
                description = f"Learn about the foundational elements, mechanisms, and real-world importance of {base} tailored for Grade {grade} students."
                keywords = f"{subject.lower()}, grade {grade}, {base.lower()}, {suffix.lower()}"
                
                topics_list.append({
                    "Topic_ID": topic_id_counter,
                    "Subject": subject,
                    "Grade": grade,
                    "Topic": topic_name,
                    "Description": description,
                    "Keywords": keywords,
                    "Difficulty": difficulty
                })
                topic_id_counter += 1
                
    # Save to CSV
    df = pd.DataFrame(topics_list)
    df.to_csv("datasets/topics.csv", index=False)
    print(f"Generated {len(df)} topics in datasets/topics.csv")
    return topics_list

def generate_quizzes(topics):
    # We need 5000+ quiz questions.
    # For each topic (1080 of them), we generate 5 questions.
    # 1080 * 5 = 5400 questions.
    quizzes = []
    question_id = 1
    
    # Types: MCQ, True/False, Fill in the Blanks, Match the Following
    for t in topics:
        topic_name = t["Topic"]
        subject = t["Subject"]
        difficulty = t["Difficulty"]
        
        # Q1: MCQ (Concept)
        quizzes.append({
            "Question_ID": question_id,
            "Topic": topic_name,
            "Question": f"What is the primary purpose of {topic_name}?",
            "Answer": f"To study and explain the properties and functions of {topic_name.split(' ')[-2]} in {subject}.",
            "Options": f"To study and explain the properties and functions of {topic_name.split(' ')[-2]} in {subject}.|To ignore the effects in the environment.|To increase industrial output only.|To create unrelated visual diagrams.",
            "Difficulty": difficulty,
            "Type": "MCQ"
        })
        question_id += 1
        
        # Q2: MCQ (Application)
        quizzes.append({
            "Question_ID": question_id,
            "Topic": topic_name,
            "Question": f"Which of the following is a direct application of {topic_name}?",
            "Answer": "Using its core principles to solve practical real-world problems.",
            "Options": "Using its core principles to solve practical real-world problems.|Avoiding it altogether in daily life.|Using it only in theoretical physics.|None of the options.",
            "Difficulty": difficulty,
            "Type": "MCQ"
        })
        question_id += 1
        
        # Q3: True/False
        tf_ans = random.choice(["True", "False"])
        statement = f"The study of {topic_name} is essential for a complete understanding of {subject} concepts." if tf_ans == "True" else f"{topic_name} has no relevance outside of Grade {t['Grade']} curriculum."
        quizzes.append({
            "Question_ID": question_id,
            "Topic": topic_name,
            "Question": f"True or False: {statement}",
            "Answer": tf_ans,
            "Options": "True|False",
            "Difficulty": difficulty,
            "Type": "True/False"
        })
        question_id += 1
        
        # Q4: Fill in the Blanks
        blank_word = topic_name.split(" ")[-2] if len(topic_name.split(" ")) > 2 else "concept"
        quizzes.append({
            "Question_ID": question_id,
            "Topic": topic_name,
            "Question": f"Complete the sentence: ________ is a core foundation of the lesson {topic_name}.",
            "Answer": blank_word,
            "Options": "",
            "Difficulty": difficulty,
            "Type": "Fill in the Blanks"
        })
        question_id += 1
        
        # Q5: Match the Following
        term_a = topic_name.split(" ")[-2]
        term_b = f"{subject} branch"
        quizzes.append({
            "Question_ID": question_id,
            "Topic": topic_name,
            "Question": f"Match the term '{term_a}' with its correct definition or category.",
            "Answer": f"{term_a} corresponds to {term_b}",
            "Options": f"{term_a} -> {term_b}|Other terms -> Other categories",
            "Difficulty": difficulty,
            "Type": "Match the Following"
        })
        question_id += 1
        
    df = pd.DataFrame(quizzes)
    df.to_csv("datasets/quizzes.csv", index=False)
    print(f"Generated {len(df)} quizzes in datasets/quizzes.csv")
    return quizzes

def generate_learning_progress(topics):
    # We need 10000+ learning progress records.
    # Columns: Student_ID, Topic, Quiz_Score, Completion_Time, Mastery_Level
    # We can generate records for 500 students, each doing ~22 topics on average.
    progress_records = []
    
    # 500 students
    student_ids = [f"STU{str(i).zfill(4)}" for i in range(1, 501)]
    
    record_count = 10500
    used_pairs = set()
    
    # Generate 10500 records
    for _ in range(record_count):
        # Prevent duplicate Student_ID + Topic combinations
        while True:
            student_id = random.choice(student_ids)
            topic = random.choice(topics)
            topic_name = topic["Topic"]
            pair = (student_id, topic_name)
            if pair not in used_pairs:
                used_pairs.add(pair)
                break
        
        # Determine score and completion time with some pattern
        # Higher grades or harder topics might take longer
        grade = topic["Grade"]
        base_time = 120 + (grade * 30) # e.g. 150s to 420s
        
        # Random quiz score (0 to 100)
        quiz_score = int(np.clip(random.gauss(75, 18), 20, 100))
        
        # High quiz score students tend to complete faster
        if quiz_score >= 85:
            completion_time = int(base_time * random.uniform(0.6, 0.9))
        elif quiz_score >= 60:
            completion_time = int(base_time * random.uniform(0.8, 1.2))
        else:
            completion_time = int(base_time * random.uniform(1.0, 1.6))
            
        # Determine Mastery Level based on score and time
        # This gives a clear, learnable boundary for the ML models
        if quiz_score >= 85 and completion_time < (base_time * 1.0):
            mastery_level = "Mastered"
        elif quiz_score >= 60:
            mastery_level = "Proficient"
        else:
            mastery_level = "Needs Improvement"
            
        progress_records.append({
            "Student_ID": student_id,
            "Topic": topic_name,
            "Quiz_Score": quiz_score,
            "Completion_Time": completion_time,
            "Mastery_Level": mastery_level
        })
        
    df = pd.DataFrame(progress_records)
    df.to_csv("datasets/progress.csv", index=False)
    print(f"Generated {len(df)} progress records in datasets/progress.csv")

if __name__ == "__main__":
    make_dirs()
    topics = generate_topics()
    generate_quizzes(topics)
    generate_learning_progress(topics)
    print("All datasets generated successfully!")
