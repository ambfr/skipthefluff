# SmartTube AI

AI-powered YouTube video discovery and quality ranking.

## Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # fill in your keys
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
cp .env.example .env      # set VITE_API_URL=http://localhost:8000
npm run dev
```

Open http://localhost:5173

## Stack
- **Frontend**: React + Vite + Tailwind CSS
- **Backend**: FastAPI + Python
- **Database**: MongoDB Atlas
- **Video Data**: YouTube Data API v3
- **AI**: Groq (Llama 3.3 70B)
