# Quick Start Guide - Fix ERR_CONNECTION_REFUSED

## ✅ Current Status

All three servers have been started in the background. They should be running now.

## 🔍 Verify Servers Are Running

Open these URLs in your browser (wait 5-10 seconds after starting):

1. **Frontend**: http://localhost:5173
   - Should show the O9 Test Automation Platform UI
   
2. **Backend API Docs**: http://localhost:8000/docs
   - Should show FastAPI Swagger documentation
   
3. **Backend Health**: http://localhost:8000/health
   - Should return: `{"status": "healthy", "api_key_configured": true}`
   
4. **Mock O9**: http://localhost:3001
   - Should show the O9 login page

## 🚀 Manual Start (If Servers Aren't Running)

If you still see `ERR_CONNECTION_REFUSED`, start the servers manually in **3 separate terminal windows**:

### Terminal 1 - Backend
```bash
cd "/Users/samvitchoudhary/Desktop/o9 automation/backend"
source venv/bin/activate
python run.py
```

**Look for:** `Uvicorn running on http://0.0.0.0:8000`

### Terminal 2 - Frontend
```bash
cd "/Users/samvitchoudhary/Desktop/o9 automation/frontend"
npm run dev
```

**Look for:** `Local: http://localhost:5173/`

### Terminal 3 - Mock O9
```bash
cd "/Users/samvitchoudhary/Desktop/o9 automation/mock-o9-website"
python3 -m http.server 3001
```

**Look for:** `Serving HTTP on 0.0.0.0 port 3001`

## ⚠️ Troubleshooting

### If Backend Won't Start:

1. **Check if .env exists:**
   ```bash
   ls backend/.env
   ```
   If missing, create it:
   ```bash
   echo "ANTHROPIC_API_KEY=your_key_here" > backend/.env
   echo "O9_MOCK_URL=http://localhost:3001" >> backend/.env
   ```

2. **Install dependencies:**
   ```bash
   cd backend
   source venv/bin/activate
   pip install -r requirements.txt --break-system-packages
   ```

3. **Check for errors in terminal output**

### If Frontend Won't Start:

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Check if port 5173 is in use:**
   ```bash
   lsof -i :5173
   ```
   If something is using it, kill it:
   ```bash
   kill -9 <PID>
   ```

### If Mock O9 Won't Start:

1. **Check if port 3001 is in use:**
   ```bash
   lsof -i :3001
   ```

2. **Try alternative:**
   ```bash
   cd mock-o9-website
   python3 serve.py
   ```

## 📋 Quick Checklist

- [ ] Python 3.12+ installed ✓
- [ ] Node.js installed ✓
- [ ] backend/.env file exists ✓
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] All three servers running
- [ ] Can access http://localhost:5173
- [ ] Can access http://localhost:8000/docs
- [ ] Can access http://localhost:3001

## 🎯 What to Do Right Now

1. **Wait 10 seconds** for servers to fully start
2. **Open your browser** and go to: http://localhost:5173
3. **If you see ERR_CONNECTION_REFUSED:**
   - Check the terminal windows where servers are running
   - Look for error messages
   - Follow the troubleshooting steps above

## 💡 Pro Tip

Keep all three terminal windows open and visible so you can see:
- Backend logs (any errors?)
- Frontend logs (compilation successful?)
- Mock O9 logs (server started?)

If any server crashes, you'll see the error immediately in its terminal.

