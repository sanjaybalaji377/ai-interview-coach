from pydantic import BaseModel
from typing import List, Optional

class StartInterviewRequest(BaseModel):
    candidate_name: str
    job_role: str
    experience_level: str

class StartInterviewResponse(BaseModel):
    interview_id: str
    question: str

class SubmitAnswerRequest(BaseModel):
    interview_id: str
    question: str
    answer: str

class SubmitAnswerResponse(BaseModel):
    score: float
    technical_score: int
    communication_score: int
    relevance_score: int
    overall_score: float
    feedback: str
    next_question: Optional[str] = None

class FinalReportResponse(BaseModel):
    candidate_name: str
    job_role: str
    overall_score: float
    strengths: List[str]
    improvement_areas: List[str]
    summary: str
