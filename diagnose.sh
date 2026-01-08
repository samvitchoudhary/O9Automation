#!/bin/bash

echo "============================================================"
echo "O9 Automation Platform - Diagnostic Script"
echo "============================================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
echo "1. Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "   ${GREEN}✓${NC} $PYTHON_VERSION"
else
    echo -e "   ${RED}✗ Python 3 not found${NC}"
    echo "   Install Python 3.12+ from python.org"
fi

# Check Node
echo ""
echo "2. Checking Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "   ${GREEN}✓${NC} $NODE_VERSION"
else
    echo -e "   ${RED}✗ Node.js not found${NC}"
    echo "   Install Node.js from nodejs.org"
fi

# Check ports
echo ""
echo "3. Checking ports..."
for port in 8000 5173 3001; do
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        PID=$(lsof -ti:$port)
        echo -e "   ${YELLOW}⚠${NC} Port $port is in use (PID: $PID)"
        echo "      Run: lsof -ti:$port | xargs kill -9"
    else
        echo -e "   ${GREEN}✓${NC} Port $port is free"
    fi
done

# Check files
echo ""
echo "4. Checking required files..."
[ -f "backend/run.py" ] && echo -e "   ${GREEN}✓${NC} backend/run.py exists" || echo -e "   ${RED}✗${NC} backend/run.py missing"
[ -f "frontend/package.json" ] && echo -e "   ${GREEN}✓${NC} frontend/package.json exists" || echo -e "   ${RED}✗${NC} frontend/package.json missing"
[ -f "mock-o9-website/index.html" ] && echo -e "   ${GREEN}✓${NC} mock-o9-website/index.html exists" || echo -e "   ${RED}✗${NC} mock-o9-website/index.html missing"

# Check .env files
echo ""
echo "5. Checking environment files..."
[ -f "backend/.env" ] && echo -e "   ${GREEN}✓${NC} backend/.env exists" || echo -e "   ${YELLOW}⚠${NC} backend/.env missing (create it with ANTHROPIC_API_KEY)"
[ -f "frontend/.env" ] && echo -e "   ${GREEN}✓${NC} frontend/.env exists" || echo -e "   ${YELLOW}⚠${NC} frontend/.env missing (optional, but recommended)"

# Check dependencies
echo ""
echo "6. Checking dependencies..."
[ -d "backend/venv" ] && echo -e "   ${GREEN}✓${NC} Backend venv exists" || echo -e "   ${RED}✗${NC} Backend venv missing (run: python3 -m venv venv)"
[ -d "frontend/node_modules" ] && echo -e "   ${GREEN}✓${NC} Frontend node_modules exists" || echo -e "   ${RED}✗${NC} Frontend node_modules missing (run: npm install)"

# Check if FastAPI is installed
echo ""
echo "7. Checking Python packages..."
if [ -d "backend/venv" ]; then
    cd backend
    source venv/bin/activate 2>/dev/null
    if python -c "import fastapi" 2>/dev/null; then
        echo -e "   ${GREEN}✓${NC} FastAPI is installed"
    else
        echo -e "   ${RED}✗${NC} FastAPI not installed (run: pip install -r requirements.txt)"
    fi
    deactivate 2>/dev/null
    cd ..
else
    echo -e "   ${YELLOW}⚠${NC} Cannot check (venv not found)"
fi

echo ""
echo "============================================================"
echo "Diagnostic complete!"
echo "============================================================"
echo ""
echo "To start all servers, open 3 separate terminals and run:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend && source venv/bin/activate && python run.py"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend && npm run dev"
echo ""
echo "Terminal 3 (Mock O9):"
echo "  cd mock-o9-website && python3 -m http.server 3001"
echo ""

