import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import (
    StartInterviewRequest, StartInterviewResponse,
    SubmitAnswerRequest, SubmitAnswerResponse,
    FinalReportResponse
)
from storage import interviews
from llm import generate_first_question, evaluate_answer, generate_report
from logger import common_logger, get_user_logger

app = FastAPI(title="AI Interview Assistant API")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_QUESTIONS = 3

@app.post("/start-interview", response_model=StartInterviewResponse)
async def start_interview(request: StartInterviewRequest):
    common_logger.info(f"Received start-interview request for candidate: {request.candidate_name}")
    try:
        interview_id = str(uuid.uuid4())
        user_logger = get_user_logger(interview_id, request.candidate_name)
        user_logger.info(f"Input to LLM (Generate Question): Role={request.job_role}, Exp={request.experience_level}")
        
        question = generate_first_question(
            request.candidate_name,
            request.job_role,
            request.experience_level
        )
        user_logger.info(f"Output from LLM (First Question): {question}")
        
        # Initialize storage
        interviews[interview_id] = {
            "candidate_name": request.candidate_name,
            "job_role": request.job_role,
            "experience_level": request.experience_level,
            "interactions": [],
            "status": "in_progress"
        }
        
        return StartInterviewResponse(
            interview_id=interview_id,
            question=question
        )
    except Exception as e:
        common_logger.error(f"Error starting interview: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/submit-answer", response_model=SubmitAnswerResponse)
async def submit_answer(request: SubmitAnswerRequest):
    if request.interview_id not in interviews:
        common_logger.error(f"submit-answer failed: Interview ID {request.interview_id} not found")
        raise HTTPException(status_code=404, detail="Interview not found")
        
    interview = interviews[request.interview_id]
    user_logger = get_user_logger(request.interview_id, interview["candidate_name"])
    
    if interview["status"] == "completed":
        user_logger.error("submit-answer failed: Interview already completed")
        raise HTTPException(status_code=400, detail="Interview already completed")
        
    interactions = interview["interactions"]
    is_last_question = len(interactions) >= (MAX_QUESTIONS - 1)
    
    user_logger.info(f"Input to LLM (Evaluate Answer): Question='{request.question}', Answer='{request.answer}'")
    
    try:
        evaluation = evaluate_answer(
            interview["job_role"],
            interview["experience_level"],
            request.question,
            request.answer,
            is_last_question
        )
        user_logger.info(f"Output from LLM (Evaluation): {evaluation}")
        
        # Calculate interaction overall score
        t_score = evaluation["technical_score"]
        c_score = evaluation["communication_score"]
        r_score = evaluation["relevance_score"]
        overall = round((t_score + c_score + r_score) / 3.0, 1)
        
        # Save interaction
        interaction = {
            "question": request.question,
            "answer": request.answer,
            "technical_score": t_score,
            "communication_score": c_score,
            "relevance_score": r_score,
            "overall_score": overall,
            "feedback": evaluation["feedback"]
        }
        interviews[request.interview_id]["interactions"].append(interaction)
        
        if is_last_question:
            interviews[request.interview_id]["status"] = "completed"
            
        return SubmitAnswerResponse(
            technical_score=t_score,
            communication_score=c_score,
            relevance_score=r_score,
            overall_score=overall,
            feedback=evaluation["feedback"],
            next_question=evaluation["next_question"]
        )
    except Exception as e:
        user_logger.error(f"Error evaluating answer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/report/{interview_id}", response_model=FinalReportResponse)
async def get_report(interview_id: str):
    if interview_id not in interviews:
        common_logger.error(f"get_report failed: Interview ID {interview_id} not found")
        raise HTTPException(status_code=404, detail="Interview not found")
        
    interview = interviews[interview_id]
    user_logger = get_user_logger(interview_id, interview["candidate_name"])
    user_logger.info("Generating final report...")
    
    # Check if report already exists to save API calls
    if "report" in interview:
        return FinalReportResponse(**interview["report"])
        
    # Generate report
    interactions = interview["interactions"]
    if not interactions:
        user_logger.error("No interactions found for this interview")
        raise HTTPException(status_code=400, detail="No interactions found for this interview")
        
    try:
        user_logger.info(f"Input to LLM (Generate Report): {len(interactions)} interactions")
        report_data = generate_report(
            interview["candidate_name"],
            interview["job_role"],
            interactions
        )
        user_logger.info(f"Output from LLM (Report Data): {report_data}")
        
        # Calculate overall score average
        total_score = sum(i.get("overall_score", 0) for i in interactions)
        overall_score = total_score / len(interactions) if interactions else 0
        
        report = {
            "candidate_name": interview["candidate_name"],
            "job_role": interview["job_role"],
            "overall_score": round(overall_score, 1),
            "strengths": report_data.get("strengths", []),
            "improvement_areas": report_data.get("improvement_areas", []),
            "summary": report_data.get("summary", "")
        }
        
        # Cache report
        interviews[interview_id]["report"] = report
        
        return FinalReportResponse(**report)
        
    except Exception as e:
        user_logger.error(f"Error generating report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Interview Assistant API"}
