#!/bin/bash
# Stop JIHClubs servers

cd /root/jihclubs

# Kill backend
if [ -f /tmp/jihclubs_backend.pid ]; then
    BACKEND_PID=$(cat /tmp/jihclubs_backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        kill $BACKEND_PID 2>/dev/null
        echo "Backend stopped (PID: $BACKEND_PID)"
    fi
    rm /tmp/jihclubs_backend.pid
fi

# Kill frontend
if [ -f /tmp/jihclubs_frontend.pid ]; then
    FRONTEND_PID=$(cat /tmp/jihclubs_frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        kill $FRONTEND_PID 2>/dev/null
        echo "Frontend stopped (PID: $FRONTEND_PID)"
    fi
    rm /tmp/jihclubs_frontend.pid
fi

# Kill any remaining processes on ports
lsof -ti:8007 | xargs kill -9 2>/dev/null || true
lsof -ti:5176 | xargs kill -9 2>/dev/null || true

echo "All servers stopped"

