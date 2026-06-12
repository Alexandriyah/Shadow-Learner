import os
import json
import re
from app.config import settings

# Attempt to import google.generativeai
try:
    import google.generativeai as genai
    gemini_installed = True
except ImportError:
    gemini_installed = False

class AIService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.client = None
        
        if gemini_installed and self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                self.client = True
                print("Gemini AI client successfully configured.")
            except Exception as e:
                print(f"Failed to configure Gemini AI: {e}")
        else:
            print("Gemini API Key missing or google-generativeai not installed. Running in offline template mode.")

    def generate_topic_content(self, topic_name: str, subject: str, grade: int) -> dict:
        """
        Generates full VisualLearn content: Explanations, Flowcharts, Mindmaps, Concept maps,
        Infographics, Flashcards, Summary notes.
        """
        if self.client:
            try:
                prompt = self._build_content_prompt(topic_name, subject, grade)
                response = self.model.generate_content(
                    prompt, 
                    generation_config={"response_mime_type": "application/json"}
                )
                content = json.loads(response.text)
                return content
            except Exception as e:
                print(f"Gemini generation error: {e}. Falling back to offline generation.")
                return self._generate_offline_fallback(topic_name, subject, grade)
        else:
            return self._generate_offline_fallback(topic_name, subject, grade)

    def generate_quiz_questions(self, topic_name: str, subject: str, grade: int, count: int = 4) -> list:
        """
        Generates MCQs, True/False, Fill in the Blanks, Match the Following dynamically
        """
        if self.client:
            try:
                prompt = self._build_quiz_prompt(topic_name, subject, grade, count)
                response = self.model.generate_content(
                    prompt,
                    generation_config={"response_mime_type": "application/json"}
                )
                return json.loads(response.text)
            except Exception as e:
                print(f"Gemini quiz generation error: {e}. Falling back to offline quizzes.")
                return self._get_offline_quizzes(topic_name, subject, grade)
        else:
            return self._get_offline_quizzes(topic_name, subject, grade)

    def chat_with_tutor(self, topic_name: str, message_history: list, new_message: str) -> str:
        """
        Interactive tutoring response tailored to the student's grade/age level
        """
        if self.client:
            try:
                prompt = self._build_tutor_prompt(topic_name, message_history, new_message)
                response = self.model.generate_content(prompt)
                return response.text.strip()
            except Exception as e:
                print(f"Gemini tutor error: {e}. Falling back to offline tutor response.")
                return self._get_offline_tutor_response(topic_name, new_message)
        else:
            return self._get_offline_tutor_response(topic_name, new_message)

    def extract_notes_from_image(self, ocr_text: str) -> dict:
        """
        Simulates OCR text analysis, returning explanations and mind maps.
        """
        if self.client:
            try:
                prompt = f"""Analyze the following OCR text extracted from a student's textbook or notebook:
                OCR Text: "{ocr_text}"
                
                Produce a JSON object with:
                1. "title": A suitable topic title.
                2. "summary": A child-friendly 3-sentence summary of the concepts.
                3. "key_points": List of 5 main takeaways.
                4. "mind_map": A JSON tree structure for graphing this concept.
                """
                response = self.model.generate_content(
                    prompt,
                    generation_config={"response_mime_type": "application/json"}
                )
                return json.loads(response.text)
            except Exception as e:
                print(f"OCR explanation failed: {e}")
                
        # Fallback summary
        return {
            "title": "Extracted Concept Notes",
            "summary": "This document covers foundational topics described in the uploaded textbook page. It outlines the core components and highlights how they work together.",
            "key_points": [
                "Primary concept definitions are introduced.",
                "Diagrams show flow and relationship structures.",
                "Real world examples help connect abstract terms to everyday life.",
                "Key statistics and formulas are highlighted in the margins.",
                "Review exercises test foundational knowledge."
            ],
            "mind_map": {
                "name": "Uploaded Notes",
                "children": [
                    {"name": "Summary Definitions"},
                    {"name": "Core Concepts"},
                    {"name": "Practical Applications"}
                ]
            }
        }

    def _build_content_prompt(self, topic_name: str, subject: str, grade: int) -> str:
        return f"""You are an elite, child-friendly tutor. Create an educational unit for "{topic_name}" (Subject: {subject}) suitable for Grade {grade}.
        Return a JSON object that adheres strictly to this schema:
        {{
          "beginner_explanation": "Simple explanation using an interactive story or analogies suitable for a 10-year-old child. Avoid jargon.",
          "intermediate_explanation": "An explanation with mid-level scientific details for middle schoolers (Grade 6-8).",
          "advanced_explanation": "A complete academic explanation detailing formulas, theories, or advanced terms.",
          "real_world_examples": [
            "Provide 3 clear real world examples of this topic in action."
          ],
          "flowchart": "Mermaid.js code starting with graph TD showing step by step process (e.g. A --> B --> C). Avoid spaces or special characters in node keys.",
          "mind_map": {{
            "name": "{topic_name}",
            "children": [
              {{ "name": "Branch 1", "children": [ {{ "name": "Sub-branch 1.1" }} ] }}
            ]
          }},
          "concept_map": [
             {{ "source": "Concept A", "relation": "results in", "target": "Concept B" }}
          ],
          "infographic": {{
             "facts": ["Fact 1", "Fact 2"],
             "statistics": ["Statistic 1", "Statistic 2"],
             "description": "Short infographic poster summary description.",
             "key_terms": ["Term A", "Term B"]
          }},
          "flashcards": [
             {{ "front": "What is...?", "back": "The answer is..." }}
          ],
          "summary": [
             "Bullet point 1", "Bullet point 2"
          ]
        }}
        """

    def _build_quiz_prompt(self, topic_name: str, subject: str, grade: int, count: int) -> str:
        return f"""Generate a list of {count} quiz questions for topic "{topic_name}" (Subject: {subject}, Grade: {grade}).
        Return a JSON list of objects matching this schema:
        [
          {{
            "question": "Question text here?",
            "type": "MCQ",
            "options": "Option A|Option B|Option C|Option D",
            "answer": "Option A",
            "difficulty": "Easy"
          }}
        ]
        Make sure you include MCQ, True/False, and Fill in the Blanks types.
        """

    def _build_tutor_prompt(self, topic_name: str, message_history: list, new_message: str) -> str:
        history_str = ""
        for m in message_history[-5:]:
            history_str += f"{m['role'].capitalize()}: {m['content']}\n"
        
        return f"""You are a patient, encouraging, and enthusiastic AI tutor teaching the topic "{topic_name}" to a child.
        Respond to the child's question using simple language, short sentences, and engaging analogies. Keep your response under 100 words.
        
        Recent chat history:
        {history_str}
        Student: {new_message}
        Tutor:"""

    def _generate_offline_fallback(self, topic_name: str, subject: str, grade: int) -> dict:
        """
        Creates template explanations for any topic dynamically
        """
        base_concept = topic_name.split("(")[0].strip()
        
        return {
            "beginner_explanation": f"Hey there! Let's think of {base_concept} like a super cool puzzle. Imagine your favorite game or playground. Just like how games have rules, {base_concept} is nature's way of organizing how things work around us. It tells us how tiny details connect to make big actions happen!",
            "intermediate_explanation": f"{base_concept} is a core topic in {subject} that governs how variables interact. In Grade {grade}, we study the mechanisms, inputs, and outputs that define {base_concept}. It forms the foundation for advanced concepts in the curriculum.",
            "advanced_explanation": f"From a rigorous perspective, {base_concept} describes the dynamics of elements in {subject} under specific boundary conditions. We analyze the quantitative variables, energy changes, and structural properties associated with this system.",
            "real_world_examples": [
                f"How {base_concept} affects our daily environment.",
                f"An experiment you can conduct at home to observe {base_concept} in action.",
                f"How scientists use {base_concept} to build new technologies."
            ],
            "flowchart": "graph TD\n  Start[Start Learning] --> Step1[Learn Core Concepts]\n  Step1 --> Step2[Examine Real World Examples]\n  Step2 --> Step3[Take the Quiz]\n  Step3 --> Success[Master the Topic!]",
            "mind_map": {
                "name": base_concept,
                "children": [
                    {"name": "Foundations", "children": [{"name": "Core Principles"}]},
                    {"name": "Applications", "children": [{"name": "Real-World Examples"}]},
                    {"name": "Assessments", "children": [{"name": "Quizzes"}, {"name": "Flashcards"}]}
                ]
            },
            "concept_map": [
                {"source": base_concept, "relation": "is a part of", "target": subject},
                {"source": "Core Principles", "relation": "explains", "target": base_concept},
                {"source": base_concept, "relation": "applies to", "target": "Real-World Examples"}
            ],
            "infographic": {
                "facts": [
                    f"{base_concept} is taught worldwide to students starting at Grade {grade}.",
                    f"Understanding {base_concept} helps build problem-solving skills."
                ],
                "statistics": [
                    "95% of students find visual maps easier to study than heavy books.",
                    "Active learning increases memory retention by 4x!"
                ],
                "description": f"A clean, visual summary card detailing the importance of {base_concept} in the {subject} syllabus.",
                "key_terms": [base_concept, subject, "Principles", "Assessment"]
            },
            "flashcards": [
                {"front": f"What is {base_concept}?", "back": f"A key topic in {subject} mapping core principles and processes."},
                {"front": f"What subject does {base_concept} belong to?", "back": f"{subject}."},
                {"front": "Why do we learn this?", "back": "To understand how concepts apply to physical, natural, or mathematical systems."}
            ],
            "summary": [
                f"{base_concept} is a central block in Grade {grade} {subject}.",
                "Visual explanations help simplify complex structures.",
                "Real world examples help make theoretical models concrete."
            ]
        }

    def _get_offline_quizzes(self, topic_name: str, subject: str, grade: int) -> list:
        base_concept = topic_name.split("(")[0].strip()
        return [
            {
                "question": f"Which of the following is true about {base_concept}?",
                "type": "MCQ",
                "options": f"It is a core part of {subject}.|It is completely useless.|It only applies to Grade 10.|It cannot be visualized.",
                "answer": f"It is a core part of {subject}.",
                "difficulty": "Easy"
            },
            {
                "question": f"True or False: Visual summaries make learning {base_concept} easier.",
                "type": "True/False",
                "options": "True|False",
                "answer": "True",
                "difficulty": "Easy"
            },
            {
                "question": f"Complete the blank: The lesson we are studying right now is ________.",
                "type": "Fill in the Blanks",
                "options": "",
                "answer": base_concept,
                "difficulty": "Medium"
            },
            {
                "question": f"Match the term '{base_concept}' with its subject branch.",
                "type": "Match the Following",
                "options": f"{base_concept} -> {subject}|Other -> Other",
                "answer": f"{base_concept} corresponds to {subject}",
                "difficulty": "Hard"
            }
        ]

    def _get_offline_tutor_response(self, topic_name: str, new_message: str) -> str:
        clean_msg = new_message.lower()
        if "why" in clean_msg:
            return f"Great question! We study {topic_name} because it helps us understand the hidden rules of the world. Knowing how things work allows us to solve everyday problems!"
        elif "how" in clean_msg:
            return f"Excellent curiosity! It works through a series of steps. Check out the flowchart tab on your screen to see exactly how each step leads to the next!"
        elif "example" in clean_msg:
            return f"Sure! Think of this like water boiling in a pot. Heat goes in, energy changes, and steam rises. That's a direct example of concepts in action!"
        else:
            return f"I love that you are asking questions! {topic_name} is all about connections. Let's look at the mind map together to see how different ideas link up!"

ai_service = AIService()
