# AI Interview Assistant - Backend

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure Environment Variables:
   Create a `.env` file in the `backend` directory and add your Google Gemini API Key:
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

4. Run the development server:
   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at `http://127.0.0.1:8000`. You can test endpoints via `http://127.0.0.1:8000/docs`.

## Deployment (Render)

1. Connect your GitHub repository to Render.
2. Create a new "Web Service".
3. Set the Root Directory to `backend` (if you structured it with a subfolder, otherwise configure the run command accordingly).
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add `GOOGLE_API_KEY` to the Environment Variables in Render.
