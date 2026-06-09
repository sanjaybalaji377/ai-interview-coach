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

class LLMError(Exception):
    pass

class LLMQuotaError(LLMError):
    pass

class LLMServiceError(LLMError):
    pass

def model_generate(prompt: str):
    model = get_model()
    try:
        return model.generate_content(prompt)
    except Exception as e:
        message = str(e)
        lowercase = message.lower()
        if "quota" in lowercase or "429" in lowercase:
            raise LLMQuotaError(
                "Gemini quota exceeded or request limit reached. Please wait, or update your API key if you have another valid key."
            ) from e
        raise LLMServiceError(
            "Gemini service error. Please check your API key and quota."
        ) from e

def generate_first_question(name: str, role: str, experience: str) -> str:
    prompt = GENERATE_QUESTION_PROMPT.format(
        candidate_name=name,
        job_role=role,
        experience_level=experience
    )
    response = model_generate(prompt)
    return response.text.strip()

def evaluate_answer(role: str, experience: str, question: str, answer: str, is_last: bool):
    prompt = EVALUATE_ANSWER_PROMPT.format(
        job_role=role,
        experience_level=experience,
        question=question,
        answer=answer,
        is_last_question=str(is_last).lower()
    )
    response = model_generate(prompt)
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
    except Exception:
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
    
    response = model_generate(prompt)
    text_response = response.text.strip()
    
    if text_response.startswith("```json"):
        text_response = text_response[7:-3]
    elif text_response.startswith("```"):
        text_response = text_response[3:-3]
        
    try:
        data = json.loads(text_response)
        return data
    except Exception:
        return {
            "strengths": ["Completed the interview"],
            "improvement_areas": ["Needs more comprehensive evaluation"],
            "summary": "Error generating detailed report."
        }
