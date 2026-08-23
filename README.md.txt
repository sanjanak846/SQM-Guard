## Setup

1. Clone the repo: `git clone https://github.com/sanjanak846/SQM-Guard.git`
2. Backend:
   cd backend
   py -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
3. Frontend:
   cd frontend
   npm install
   npm start
4. Install Ollama from ollama.com, then run: ollama pull tinyllama