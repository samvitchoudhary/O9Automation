#!/bin/bash

echo "Stopping all services..."

# Read PIDs from files
if [ -f "logs/backend.pid" ]; then
    kill $(cat logs/backend.pid) 2>/dev/null
    rm logs/backend.pid
    echo "✓ Backend stopped"
fi

if [ -f "logs/frontend.pid" ]; then
    kill $(cat logs/frontend.pid) 2>/dev/null
    rm logs/frontend.pid
    echo "✓ Frontend stopped"
fi

if [ -f "logs/mock-o9.pid" ]; then
    kill $(cat logs/mock-o9.pid) 2>/dev/null
    rm logs/mock-o9.pid
    echo "✓ Mock O9 stopped"
fi

# Fallback: kill by port
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:5173 | xargs kill -9 2>/dev/null
lsof -ti:3001 | xargs kill -9 2>/dev/null

echo "All services stopped"

