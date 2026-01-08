# Manual Server Start Guide

## ⚠️ IMPORTANT: Run These Commands in 3 SEPARATE Terminal Windows

You need to open **3 different terminal windows** and run one command in each. **DO NOT close any terminal** - each server needs to keep running.

---

## Terminal 1: Backend Server (Port 8000)

**Open a new terminal window** and run:

```bash
cd "/Users/samvitchoudhary/Desktop/o9 automation/backend"
source venv/bin/activate
python run.py
```

### What to Look For:

**✅ SUCCESS looks like:**
```
============================================================
Starting O9 Test Automation Platform Backend
============================================================
✓ Database initialized
✓ ANTHROPIC_API_KEY loaded (starts with: sk-ant-...)
✓ Mock O9 URL configured: http://localhost:3001
============================================================
Backend is ready!
API Docs: http://localhost:8000/docs
============================================================
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**❌ ERRORS to watch for:**

1. **"No module named 'fastapi'"**
   ```bash
   # Fix: Install dependencies
   pip install -r requirements.txt --break-system-packages
   ```

2. **"ANTHROPIC_API_KEY not found"**
   ```bash
   # Fix: Create .env file
   echo "ANTHROPIC_API_KEY=your_actual_key_here" > .env
   echo "O9_MOCK_URL=http://localhost:3001" >> .env
   ```

3. **"Address already in use"**
   ```bash
   # Fix: Kill process on port 8000
   lsof -ti:8000 | xargs kill -9
   ```

4. **"Database error"**
   ```bash
   # Fix: Delete and recreate database
   rm test_cases.db
   python run.py
   ```

**Keep this terminal open!** The backend must keep running.

---

## Terminal 2: Frontend Server (Port 5173)

**Open a NEW terminal window** (keep Terminal 1 running!) and run:

```bash
cd "/Users/samvitchoudhary/Desktop/o9 automation/frontend"
npm run dev
```

### What to Look For:

**✅ SUCCESS looks like:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

**❌ ERRORS to watch for:**

1. **"command not found: npm"**
   ```bash
   # Fix: Install Node.js
   # Mac: brew install node
   # Or download from nodejs.org
   ```

2. **"Cannot find module"**
   ```bash
   # Fix: Install dependencies
   npm install
   ```

3. **"Port 5173 is already in use"**
   ```bash
   # Fix: Kill process on port 5173
   lsof -ti:5173 | xargs kill -9
   ```

4. **"ECONNREFUSED" or "Failed to fetch"**
   - This means backend (Terminal 1) is not running
   - Go back to Terminal 1 and make sure backend started successfully

**Keep this terminal open!** The frontend must keep running.

---

## Terminal 3: Mock O9 Website (Port 3001)

**Open a NEW terminal window** (keep Terminals 1 & 2 running!) and run:

```bash
cd "/Users/samvitchoudhary/Desktop/o9 automation/mock-o9-website"
python3 -m http.server 3001
```

### What to Look For:

**✅ SUCCESS looks like:**
```
Serving HTTP on 0.0.0.0 port 3001 (http://0.0.0.0:3001/) ...
```

**❌ ERRORS to watch for:**

1. **"Address already in use"**
   ```bash
   # Fix: Kill process on port 3001
   lsof -ti:3001 | xargs kill -9
   ```

2. **"command not found: python3"**
   ```bash
   # Fix: Try python instead
   python -m http.server 3001
   ```

**Keep this terminal open!** The mock O9 server must keep running.

---

## Verify All Servers Are Running

After starting all 3 terminals, **wait 10 seconds**, then open these URLs in your browser:

1. **Frontend**: http://localhost:5173
   - Should show the O9 Test Automation Platform UI
   - If you see "ERR_CONNECTION_REFUSED", check Terminal 2 for errors

2. **Backend API Docs**: http://localhost:8000/docs
   - Should show FastAPI Swagger documentation
   - If you see "ERR_CONNECTION_REFUSED", check Terminal 1 for errors

3. **Backend Health**: http://localhost:8000/health
   - Should return: `{"status": "healthy", "api_key_configured": true}`
   - If you see "ERR_CONNECTION_REFUSED", check Terminal 1 for errors

4. **Mock O9**: http://localhost:3001
   - Should show the O9 login page
   - If you see "ERR_CONNECTION_REFUSED", check Terminal 3 for errors

---

## Common Issues & Solutions

### Issue 1: Backend Won't Start

**Symptom:** Terminal 1 shows errors or exits immediately

**Solutions:**
```bash
# 1. Check if dependencies are installed
cd backend
source venv/bin/activate
pip list | grep fastapi
# If not found:
pip install -r requirements.txt --break-system-packages

# 2. Check if .env exists
ls -la .env
# If missing:
echo "ANTHROPIC_API_KEY=your_key_here" > .env
echo "O9_MOCK_URL=http://localhost:3001" >> .env

# 3. Check for port conflicts
lsof -i :8000
# If something is using it:
lsof -ti:8000 | xargs kill -9
```

### Issue 2: Frontend Won't Start

**Symptom:** Terminal 2 shows errors or exits immediately

**Solutions:**
```bash
# 1. Check if node_modules exists
cd frontend
ls node_modules
# If missing:
npm install

# 2. Check for port conflicts
lsof -i :5173
# If something is using it:
lsof -ti:5173 | xargs kill -9
```

### Issue 3: "Failed to fetch" in Browser Console

**Symptom:** Frontend loads but can't connect to backend

**Solutions:**
1. **Check Terminal 1** - Is backend actually running?
2. **Check Terminal 2** - Look for CORS errors
3. **Verify backend URL:**
   ```bash
   # In frontend directory
   cat .env
   # Should show: VITE_API_URL=http://localhost:8000
   ```

### Issue 4: All Servers Start But Nothing Works

**Symptom:** All 3 terminals show "running" but browser shows errors

**Solutions:**
1. **Hard refresh browser:** Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
2. **Check browser console:** Press F12, look for errors
3. **Check all 3 terminals:** Look for any error messages
4. **Verify ports are actually listening:**
   ```bash
   lsof -i :8000  # Backend
   lsof -i :5173  # Frontend
   lsof -i :3001  # Mock O9
   ```

---

## Quick Diagnostic Commands

Run these to check your setup:

```bash
# Check Python version
python3 --version
# Should show: Python 3.12.x

# Check Node version
node --version
# Should show: v22.x.x

# Check if ports are free
lsof -i :8000 || echo "Port 8000 is free"
lsof -i :5173 || echo "Port 5173 is free"
lsof -i :3001 || echo "Port 3001 is free"

# Check if files exist
ls backend/run.py && echo "✓ Backend run.py exists"
ls frontend/package.json && echo "✓ Frontend package.json exists"
ls mock-o9-website/index.html && echo "✓ Mock O9 index.html exists"

# Check if .env exists
ls backend/.env && echo "✓ Backend .env exists" || echo "✗ Backend .env missing"
ls frontend/.env && echo "✓ Frontend .env exists" || echo "✗ Frontend .env missing (optional)"
```

---

## Step-by-Step Checklist

Follow these steps **in order**:

- [ ] Open Terminal 1
- [ ] Navigate to backend directory
- [ ] Activate virtual environment
- [ ] Start backend server
- [ ] Verify backend shows "Uvicorn running"
- [ ] **Keep Terminal 1 open**

- [ ] Open Terminal 2 (NEW terminal)
- [ ] Navigate to frontend directory
- [ ] Start frontend server
- [ ] Verify frontend shows "Local: http://localhost:5173"
- [ ] **Keep Terminal 2 open**

- [ ] Open Terminal 3 (NEW terminal)
- [ ] Navigate to mock-o9-website directory
- [ ] Start mock server
- [ ] Verify mock shows "Serving HTTP on 0.0.0.0 port 3001"
- [ ] **Keep Terminal 3 open**

- [ ] Wait 10 seconds
- [ ] Open browser to http://localhost:5173
- [ ] Should see the O9 Test Automation Platform

---

## Still Having Issues?

If you're still seeing errors after following all steps:

1. **Copy the exact error message** from the terminal
2. **Check which terminal** the error is in (1, 2, or 3)
3. **Take a screenshot** of the error
4. **Check the browser console** (F12) for any additional errors

The error messages in the terminals will tell you exactly what's wrong!

