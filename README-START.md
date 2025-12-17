# Как запустить проект

## Вариант 1: Запуск в отдельных терминалах (Рекомендуется)

### Терминал 1 - Backend:
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

### Терминал 2 - Frontend:
```bash
cd frontend
npm run dev
```

## Вариант 2: Использование скриптов

### Backend:
```bash
./start-backend.sh
```

### Frontend:
```bash
./start-frontend.sh
```

## Вариант 3: Запуск в фоне (одна команда)

### Backend (в фоне):
```bash
cd backend && source venv/bin/activate && uvicorn main:app --reload &
```

### Frontend (в фоне):
```bash
cd frontend && npm run dev &
```

## Проверка работы:

- Backend API: http://localhost:8000
- Backend Docs: http://localhost:8000/docs
- Frontend: http://localhost:5173

## Остановка серверов:

Нажмите `Ctrl+C` в терминале, где запущен сервер, или:

```bash
# Остановить backend
lsof -ti:8000 | xargs kill -9

# Остановить frontend
lsof -ti:5173 | xargs kill -9
```


