#!/bin/bash
cd "$(dirname "$0")/backend"
source venv/bin/activate
echo "🚀 Запуск Backend сервера на http://localhost:8000"
uvicorn main:app --reload


