# AI Interview Practice Assistant

A simple full-stack application built with FastAPI and React to simulate technical interviews using Google's Gemini LLM.

## Overview
This application allows a user to select a job role and experience level, receive AI-generated interview questions, answer them, and get real-time feedback with scores. At the end, a comprehensive report is generated.

**LLM Provider & Model Used**: Google Gemini API via `google-generativeai` (`gemini-2.5-flash`)
**Storage**: In-memory dictionary

### Implemented Bonus Features
- **Conversation History**: All Q&A pairs are persistently stored per interview session.
- **Multiple Scoring Categories**: Instead of a single score, the LLM evaluates Technical Knowledge, Communication, and Relevance separately (1-10) and calculates an overall average.

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
