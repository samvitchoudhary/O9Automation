#!/bin/bash

echo "============================================================"
echo "Starting O9 Test Automation Platform"
echo "============================================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${RED}✗ Port $1 is already in use${NC}"
        return 1
    else
        echo -e "${GREEN}✓ Port $1 is available${NC}"
        return 0
    fi
}

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

# Check ports
echo ""
echo "Checking ports..."
check_port 8000 || exit 1
check_port 5173 || exit 1
check_port 3001 || exit 1

# Create logs directory
mkdir -p logs

# Start backend
echo ""
echo "============================================================"
echo "Starting Backend (Port 8000)..."
echo "============================================================"
cd backend
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠ Warning: backend/.env file not found${NC}"
    echo "Create it with: ANTHROPIC_API_KEY=your_key_here"
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

python3 run.py > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend started (PID: $BACKEND_PID)"
cd ..

# Wait for backend to start
sleep 3

# Start frontend
echo ""
echo "============================================================"
echo "Starting Frontend (Port 5173)..."
echo "============================================================"
cd frontend
npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend started (PID: $FRONTEND_PID)"
cd ..

# Wait for frontend to start
sleep 3

# Start mock O9 website
echo ""
echo "============================================================"
echo "Starting Mock O9 Website (Port 3001)..."
echo "============================================================"
cd mock-o9-website
python3 serve.py > ../logs/mock-o9.log 2>&1 &
MOCK_PID=$!
echo "Mock O9 started (PID: $MOCK_PID)"
cd ..

echo ""
echo "============================================================"
echo "All services started successfully!"
echo "============================================================"
echo ""
echo "Access URLs:"
echo "  Frontend:  http://localhost:5173"
echo "  Backend:   http://localhost:8000"
echo "  API Docs:  http://localhost:8000/docs"
echo "  Mock O9:   http://localhost:3001"
echo ""
echo "Process IDs:"
echo "  Backend:   $BACKEND_PID"
echo "  Frontend:  $FRONTEND_PID"
echo "  Mock O9:   $MOCK_PID"
echo ""
echo "To stop all services, run: ./stop-all.sh"
echo "Or press Ctrl+C"
echo "============================================================"

# Save PIDs
echo $BACKEND_PID > logs/backend.pid
echo $FRONTEND_PID > logs/frontend.pid
echo $MOCK_PID > logs/mock-o9.pid

# Wait for Ctrl+C
trap "echo ''; echo 'Stopping all services...'; kill $BACKEND_PID $FRONTEND_PID $MOCK_PID 2>/dev/null; exit 0" INT
wait

