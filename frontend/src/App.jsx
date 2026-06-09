import { useState } from 'react'
import './index.css'

function App() {
  const [candidate, setCandidate] = useState({ name: '', role: '', experience: '' })
  const [interviewId, setInterviewId] = useState(null)
  const [currentQuestion, setCurrentQuestion] = useState(null)
  const [answer, setAnswer] = useState('')
  const [feedback, setFeedback] = useState(null)
  const [report, setReport] = useState(null)
  const [isCompleted, setIsCompleted] = useState(false)
  const [loading, setLoading] = useState(false)

  const API_URL = 'http://localhost:8000'

  const startInterview = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      const res = await fetch(`${API_URL}/start-interview`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          candidate_name: candidate.name,
          job_role: candidate.role,
          experience_level: candidate.experience
        })
      })
      const data = await res.json()
      setInterviewId(data.interview_id)
      setCurrentQuestion(data.question)
    } catch (err) {
      console.error(err)
      alert("Error starting interview")
    }
    setLoading(false)
  }

  const submitAnswer = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      const res = await fetch(`${API_URL}/submit-answer`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          interview_id: interviewId,
          question: currentQuestion,
          answer: answer
        })
      })
      const data = await res.json()
      setFeedback({ 
        technical_score: data.technical_score,
        communication_score: data.communication_score,
        relevance_score: data.relevance_score,
        overall_score: data.overall_score,
        text: data.feedback 
      })
      
      if (data.next_question) {
        setCurrentQuestion(data.next_question)
        setAnswer('')
      } else {
        setIsCompleted(true)
      }
    } catch (err) {
      console.error(err)
      alert("Error submitting answer")
    }
    setLoading(false)
  }

  const fetchReport = async () => {
    setLoading(true)
    try {
      const res = await fetch(`${API_URL}/report/${interviewId}`)
      const data = await res.json()
      setReport(data)
    } catch (err) {
      console.error(err)
      alert("Error fetching report")
    }
    setLoading(false)
  }

  return (
    <div className="app-container">
      <h1>AI Interview Assistant</h1>
      
      {!interviewId && !report && (
        <form onSubmit={startInterview}>
          <div className="form-group">
            <label>Candidate Name</label>
            <input 
              type="text" placeholder="e.g. Rahul" required
              value={candidate.name} onChange={e => setCandidate({...candidate, name: e.target.value})} 
            />
          </div>
          <div className="form-group">
            <label>Job Role</label>
            <input 
              type="text" placeholder="e.g. Python Developer" required
              value={candidate.role} onChange={e => setCandidate({...candidate, role: e.target.value})} 
            />
          </div>
          <div className="form-group">
            <label>Experience Level</label>
            <input 
              type="text" placeholder="e.g. Fresher / 2 Years" required
              value={candidate.experience} onChange={e => setCandidate({...candidate, experience: e.target.value})} 
            />
          </div>
          <button type="submit" disabled={loading}>
            {loading ? 'Initializing Interview...' : 'Start Interview'}
          </button>
        </form>
      )}

      {interviewId && !isCompleted && !report && (
        <div>
          {feedback && (
            <div className="feedback-card">
              <h4>Previous Answer Feedback</h4>
              <div className="scores-grid">
                <div className="score-item"><span>Technical</span><strong>{feedback.technical_score}/10</strong></div>
                <div className="score-item"><span>Communication</span><strong>{feedback.communication_score}/10</strong></div>
                <div className="score-item"><span>Relevance</span><strong>{feedback.relevance_score}/10</strong></div>
                <div className="score-item"><span>Overall</span><strong>{feedback.overall_score}/10</strong></div>
              </div>
              <p>{feedback.text}</p>
            </div>
          )}
          
          <div className="question-box">
            <h3>Question</h3>
            <p>{currentQuestion}</p>
          </div>

          <form onSubmit={submitAnswer}>
            <div className="form-group">
              <label>Your Answer</label>
              <textarea 
                rows="6" placeholder="Type your answer here..." required
                value={answer} onChange={e => setAnswer(e.target.value)}
              />
            </div>
            <button type="submit" disabled={loading}>
              {loading ? 'Evaluating...' : 'Submit Answer'}
            </button>
          </form>
        </div>
      )}

      {isCompleted && !report && (
        <div>
          {feedback && (
            <div className="feedback-card">
              <h4>Final Answer Feedback</h4>
              <div className="scores-grid">
                <div className="score-item"><span>Technical</span><strong>{feedback.technical_score}/10</strong></div>
                <div className="score-item"><span>Communication</span><strong>{feedback.communication_score}/10</strong></div>
                <div className="score-item"><span>Relevance</span><strong>{feedback.relevance_score}/10</strong></div>
                <div className="score-item"><span>Overall</span><strong>{feedback.overall_score}/10</strong></div>
              </div>
              <p>{feedback.text}</p>
            </div>
          )}
          <div className="question-box" style={{ textAlign: 'center' }}>
            <h3>Interview Completed!</h3>
            <p>You've answered all the questions. Click below to generate your final comprehensive report.</p>
          </div>
          <button onClick={fetchReport} disabled={loading}>
            {loading ? 'Generating Report...' : 'Get Final Report'}
          </button>
        </div>
      )}

      {report && (
        <div className="report-card">
          <div className="report-header">
            <div>
              <h2>Final Interview Report</h2>
              <p style={{color: 'var(--text-muted)'}}>{report.candidate_name} • {report.job_role}</p>
            </div>
            <div className="score-item" style={{background: 'var(--primary)', padding: '1rem'}}>
              <span style={{color: 'rgba(255,255,255,0.8)'}}>Overall Score</span>
              <strong style={{fontSize: '2rem'}}>{report.overall_score}/10</strong>
            </div>
          </div>
          
          <div className="report-section">
            <h3>Strengths</h3>
            <ul>{report.strengths.map((s, i) => <li key={i}>{s}</li>)}</ul>
          </div>
          
          <div className="report-section">
            <h3>Areas for Improvement</h3>
            <ul>{report.improvement_areas.map((s, i) => <li key={i}>{s}</li>)}</ul>
          </div>
          
          <div className="report-section">
            <h3>Summary</h3>
            <p style={{lineHeight: 1.6, color: 'var(--text-muted)'}}>{report.summary}</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default App
