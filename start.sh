#!/bin/bash

echo "============================================================"
echo "Starting O9 Test Automation Platform"
echo "============================================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 is not installed${NC}"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}✗ Node.js is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python and Node.js are installed${NC}"
echo ""

# Check if .env files exist
if [ ! -f "backend/.env" ]; then
    echo -e "${YELLOW}⚠ Warning: backend/.env file not found${NC}"
    echo "Create it with: ANTHROPIC_API_KEY=your_key_here"
    echo ""
fi

# Start backend
echo "============================================================"
echo "Starting Backend (Port 8000)..."
echo "============================================================"
cd backend
if [ -d "venv" ]; then
    source venv/bin/activate
fi
python3 run.py &
BACKEND_PID=$!
echo "Backend started (PID: $BACKEND_PID)"
cd ..
sleep 3

# Start frontend
echo ""
echo "============================================================"
echo "Starting Frontend (Port 5173)..."
echo "============================================================"
cd frontend
npm run dev &
FRONTEND_PID=$!
echo "Frontend started (PID: $FRONTEND_PID)"
cd ..
sleep 3

# Start mock O9 website
echo ""
echo "============================================================"
echo "Starting Mock O9 Website (Port 3001)..."
echo "============================================================"
cd mock-o9-website
python3 -m http.server 3001 &
MOCK_PID=$!
echo "Mock O9 started (PID: $MOCK_PID)"
cd ..

echo ""
echo "============================================================"
echo "All services started!"
echo "============================================================"
echo ""
echo "Access URLs:"
echo "  Frontend:  http://localhost:5173"
echo "  Backend:   http://localhost:8000"
echo "  API Docs:  http://localhost:8000/docs"
echo "  Health:    http://localhost:8000/health"
echo "  Mock O9:   http://localhost:3001"
echo ""
echo "Process IDs:"
echo "  Backend:   $BACKEND_PID"
echo "  Frontend:  $FRONTEND_PID"
echo "  Mock O9:   $MOCK_PID"
echo ""
echo "Press Ctrl+C to stop all services"
echo "============================================================"

# Wait for Ctrl+C
trap "echo ''; echo 'Stopping all services...'; kill $BACKEND_PID $FRONTEND_PID $MOCK_PID 2>/dev/null; exit 0" INT
wait

