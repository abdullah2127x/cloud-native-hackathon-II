I signin with the correct credentials and got signin and get the dashboard ot the browser and on the frontend server logs are:
```


> frontend@0.1.0 dev
> next dev

▲ Next.js 16.1.3 (Turbopack)
- Local:         http://localhost:3000
- Network:       http://192.168.1.7:3000
- Environments: .env.local, .env

✓ Starting...
✓ Ready in 3.9s
○ Compiling /sign-in ...
 GET /sign-in 200 in 8.2s (compile: 7.4s, render: 807ms)
 GET /sign-in?returnUrl=%2Fdashboard 200 in 8.1s (compile: 7.5s, render: 598ms)
 POST /api/auth/sign-in/email 200 in 6.7s (compile: 4.7s, render: 2.0s)
 GET /api/auth/token 200 in 773ms (compile: 43ms, render: 730ms)
 GET /dashboard 200 in 1826ms (compile: 1746ms, render: 79ms)
 GET /api/auth/get-session 200 in 744ms (compile: 20ms, render: 724ms)
 GET /api/auth/get-session 200 in 741ms (compile: 19ms, render: 722ms)
 GET /api/auth/.well-known/jwks.json 200 in 962ms (compile: 37ms, render: 925ms)
 GET /api/auth/get-session 200 in 788ms (compile: 49ms, render: 739ms)
```

and at the same time the log on the backend server is :
```
(todo-backend) PS D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend> uv run uvicorn src.main:app --reload --port 8000
INFO:     Will watch for changes in these directories: ['D:\\AbdullahQureshi\\workspace\\Hackathon-2025\\hackathon-2\\todo-in-memory-console-app\\backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [25588] using StatReload
INFO:     Started server process [21856]
INFO:     Waiting for application startup.
2026-01-17 20:24:59,977 - src.main - INFO - Starting up Todo Backend API...
2026-01-17 20:25:04,414 - src.main - INFO - Database tables created/verified
INFO:     Application startup complete.
2026-01-17 20:27:28,400 - src.middleware.logging - INFO - GET /api/todos
2026-01-17 20:27:28,402 - src.middleware.logging - INFO - GET /api/todos status=307 duration=0.003s
INFO:     127.0.0.1:58848 - "GET /api/todos HTTP/1.1" 307 Temporary Redirect
2026-01-17 20:27:28,410 - src.middleware.logging - INFO - GET /api/todos
2026-01-17 20:27:28,411 - src.middleware.logging - INFO - GET /api/todos status=307 duration=0.001s
INFO:     127.0.0.1:58848 - "GET /api/todos HTTP/1.1" 307 Temporary Redirect
2026-01-17 20:27:28,415 - src.middleware.logging - INFO - GET /api/todos/
2026-01-17 20:27:30,131 - src.middleware.logging - INFO - GET /api/todos/ status=200 duration=1.717s
INFO:     127.0.0.1:58848 - "GET /api/todos/ HTTP/1.1" 200 OK
2026-01-17 20:27:30,134 - src.middleware.logging - INFO - GET /api/todos/
2026-01-17 20:27:31,977 - src.middleware.logging - INFO - GET /api/todos/ status=200 duration=1.843s
INFO:     127.0.0.1:54497 - "GET /api/todos/ HTTP/1.1" 200 OK
```


now the next part is 
when i try to sign in again with the incorrect credentials so the logs: 