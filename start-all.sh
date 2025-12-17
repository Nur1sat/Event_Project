#!/bin/bash
# Navigate to project directory
cd /root/jihclubs

# Start backend
cd backend
source venv/bin/activate
nohup uvicorn main:app --reload --host 0.0.0.0 --port 8007 > ../backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend started with PID: $BACKEND_PID"

# Start frontend
cd ../frontend
nohup npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend started with PID: $FRONTEND_PID"

# Save PIDs for systemd
echo $BACKEND_PID > /tmp/jihclubs_backend.pid
echo $FRONTEND_PID > /tmp/jihclubs_frontend.pid

# Wait for all background processes
wait
