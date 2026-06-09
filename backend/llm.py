import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from prompts import GENERATE_QUESTION_PROMPT, EVALUATE_ANSWER_PROMPT, GENERATE_REPORT_PROMPT

load_dotenv()
# Configure the API key. In production, ensure GOOGLE_API_KEY is set.
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_model():
    return genai.GenerativeModel("gemini-2.5-flash")

def generate_first_question(name: str, role: str, experience: str) -> str:
    prompt = GENERATE_QUESTION_PROMPT.format(
        candidate_name=name,
        job_role=role,
        experience_level=experience
    )
    model = get_model()
    response = model.generate_content(prompt)
    return response.text.strip()

def evaluate_answer(role: str, experience: str, question: str, answer: str, is_last: bool):
    prompt = EVALUATE_ANSWER_PROMPT.format(
        job_role=role,
        experience_level=experience,
        question=question,
        answer=answer,
        is_last_question=str(is_last).lower()
    )
    model = get_model()
    response = model.generate_content(prompt)
    text_response = response.text.strip()
    
    if text_response.startswith("```json"):
        text_response = text_response[7:-3]
    elif text_response.startswith("```"):
        text_response = text_response[3:-3]
        
    try:
        data = json.loads(text_response)
        if "technical_score" not in data: data["technical_score"] = 5
        if "communication_score" not in data: data["communication_score"] = 5
        if "relevance_score" not in data: data["relevance_score"] = 5
        if "feedback" not in data: data["feedback"] = "No feedback generated."
        if "next_question" not in data: data["next_question"] = None
        return data
    except Exception as e:
        return {
            "technical_score": 5,
            "communication_score": 5,
            "relevance_score": 5,
            "feedback": "Failed to evaluate answer properly.",
            "next_question": "Can you elaborate more on your previous experience?" if not is_last else None
        }

def generate_report(name: str, role: str, interactions: list):
    transcript = ""
    for i, interaction in enumerate(interactions):
        transcript += f"Q{i+1}: {interaction['question']}\n"
        transcript += f"A{i+1}: {interaction['answer']}\n"
        transcript += f"Score - Technical: {interaction.get('technical_score', 0)}, Communication: {interaction.get('communication_score', 0)}, Relevance: {interaction.get('relevance_score', 0)}, Overall: {interaction.get('overall_score', 0)}\n\n"
        
    prompt = GENERATE_REPORT_PROMPT.format(
        candidate_name=name,
        job_role=role,
        transcript=transcript
    )
    
    model = get_model()
    response = model.generate_content(prompt)
    text_response = response.text.strip()
    
    if text_response.startswith("```json"):
        text_response = text_response[7:-3]
    elif text_response.startswith("```"):
        text_response = text_response[3:-3]
        
    try:
        data = json.loads(text_response)
        return data
    except Exception as e:
        return {
            "strengths": ["Completed the interview"],
            "improvement_areas": ["Needs more comprehensive evaluation"],
            "summary": "Error generating detailed report."
        }
