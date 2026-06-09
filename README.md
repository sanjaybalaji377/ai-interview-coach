# AI Interview Practice Assistant

A simple full-stack application built with FastAPI and React to simulate technical interviews using Google's Gemini LLM.

## Overview
This application allows a user to select a job role and experience level, receive AI-generated interview questions, answer them, and get real-time feedback with scores. At the end, a comprehensive report is generated.

**LLM Provider & Model Used**: Google Gemini API via `google-generativeai` (`gemini-2.5-flash`)
**Storage**: In-memory dictionary

### Implemented Bonus Features
- **Conversation History**: All Q&A pairs are persistently stored per interview session.
- **Multiple Scoring Categories**: Instead of a single score, the LLM evaluates Technical Knowledge, Communication, and Relevance separately (1-10) and calculates an overall average.

## Live Links

- **Frontend**: https://ai-interview-coach-xi-seven.vercel.app
- **Backend API**: https://ai-interview-coach-dbej.onrender.com
- **API Documentation**: https://ai-interview-coach-dbej.onrender.com/docs

*Note: The backend is hosted on Render free tier, so the first request may take 30–60 seconds due to cold start.*

## Interview Flow

1. **User enters candidate details**: Candidate name, job role, and experience level
2. **Backend generates first question**: Uses Gemini to create a contextual interview question
3. **User submits answer**: Candidate provides their response to each question
4. **Backend evaluates answer**: Gemini evaluates based on:
   - **Technical Knowledge** (1-10): Depth and accuracy of technical concepts
   - **Communication** (1-10): Clarity and articulation
   - **Relevance** (1-10): How well the answer addresses the question
5. **Calculate score**: Backend averages the three scores for an overall score
6. **After 3 questions**: Final comprehensive report is generated with strengths and improvement areas

## Tech Stack
- **Backend**: FastAPI, Pydantic, google-generativeai, python-dotenv
- **Frontend**: React (Vite)

## Local Setup Instructions

### Backend (FastAPI)
1. `cd backend`
2. `python -m venv venv`
3. Activate virtual environment (`venv\Scripts\activate` on Windows, `source venv/bin/activate` on Mac/Linux)
4. `pip install -r requirements.txt`
5. Create a `.env` file and add your API key: `GOOGLE_API_KEY=your_key`
6. `uvicorn main:app --reload`

The backend will run on `http://127.0.0.1:8000`

### Frontend (React)
1. `cd frontend`
2. `npm install`
3. `npm run dev`

The frontend will run on `http://localhost:5173`. Open it in your browser to start the interview!
