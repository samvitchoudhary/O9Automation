# Quick Setup Guide

## Step 1: Create Environment Files

### Backend Environment File

Create `backend/.env` file:

```bash
cd backend
cat > .env << EOF
ANTHROPIC_API_KEY=your_actual_api_key_here
O9_MOCK_URL=http://localhost:3001
DATABASE_URL=sqlite:///test_cases.db
EOF
```

**IMPORTANT**: Replace `your_actual_api_key_here` with your real Anthropic API key!

### Frontend Environment File

Create `frontend/.env` file:

```bash
cd frontend
cat > .env << EOF
VITE_API_URL=http://localhost:8000
EOF
```

## Step 2: Install Dependencies

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt --break-system-packages
```

### Frontend

```bash
cd frontend
npm install
```

## Step 3: Start All Services

### Option 1: Use Startup Script (Recommended)

**Linux/Mac:**
```bash
./start-all.sh
```

**Windows:**
```bash
start-all.bat
```

### Option 2: Manual Start (3 Separate Terminals)

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python run.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Terminal 3 - Mock O9:**
```bash
cd mock-o9-website
python3 serve.py
```

## Step 4: Verify Everything is Running

Open these URLs in your browser:

1. **Frontend**: http://localhost:5173
   - Should show the O9 Test Automation Platform
   
2. **Backend API Docs**: http://localhost:8000/docs
   - Should show FastAPI Swagger UI
   
3. **Backend Health**: http://localhost:8000/health
   - Should return `{"status": "healthy", "api_key_configured": true}`
   
4. **Mock O9**: http://localhost:3001
   - Should show the O9 login page

## Troubleshooting

### Port Already in Use

**Kill processes on ports:**
```bash
# Linux/Mac
lsof -ti:8000 | xargs kill -9
lsof -ti:5173 | xargs kill -9
lsof -ti:3001 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Backend Not Starting

1. Check if `.env` file exists in `backend/`
2. Verify API key is set correctly
3. Check logs: `logs/backend.log`

### Frontend Not Connecting

1. Check if backend is running on port 8000
2. Verify `frontend/.env` has `VITE_API_URL=http://localhost:8000`
3. Hard refresh browser: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)

### CORS Errors

The backend is configured to allow requests from:
- http://localhost:5173
- http://127.0.0.1:5173
- http://localhost:3000
- http://127.0.0.1:3000

If you still see CORS errors, check the browser console for details.

## Next Steps

Once everything is running:

1. Create a test case in the frontend
2. Generate a Selenium script
3. Run the automation against the mock O9 website

Enjoy testing! 🚀

