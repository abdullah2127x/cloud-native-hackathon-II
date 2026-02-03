(backend) PS D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend> uv run uvicorn src.main:app --port 8000 --reload
INFO:     Will watch for changes in these directories: ['D:\\AbdullahQureshi\\workspace\\Hackathon-2025\\hackathon-2\\todo-in-memory-console-app\\backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [7572] using StatReload
INFO:     Started server process [17656]
INFO:     Waiting for application startup.
2026-01-25 10:44:27,858 - src.main - INFO - Starting up Todo Backend API...
2026-01-25 10:44:27,859 - src.db.database - INFO - Creating database tables...
2026-01-25 10:44:33,037 - src.db.database - INFO - Database tables created successfully
2026-01-25 10:44:33,037 - src.main - INFO - Database tables created/verified
INFO:     Application startup complete.
2026-01-25 10:44:33,056 - src.middleware.logging - INFO - GET /
2026-01-25 10:44:33,060 - src.middleware.logging - INFO - GET / status=200 duration=0.004s
INFO:     127.0.0.1:49727 - "GET / HTTP/1.1" 200 OK
2026-01-25 10:45:04,682 - src.middleware.logging - INFO - GET /docs
2026-01-25 10:45:04,682 - src.middleware.logging - INFO - GET /docs status=200 duration=0.000s
INFO:     127.0.0.1:50483 - "GET /docs HTTP/1.1" 200 OK
2026-01-25 10:45:05,019 - src.middleware.logging - INFO - GET /openapi.json
2026-01-25 10:45:05,073 - src.middleware.logging - INFO - GET /openapi.json status=200 duration=0.054s
INFO:     127.0.0.1:50483 - "GET /openapi.json HTTP/1.1" 200 OK
2026-01-25 10:45:28,330 - src.middleware.logging - INFO - GET /api/todos
2026-01-25 10:45:28,330 - src.middleware.logging - INFO - GET /api/tags
2026-01-25 10:45:28,330 - src.middleware.logging - INFO - GET /api/todos status=307 duration=0.000s
2026-01-25 10:45:28,330 - src.middleware.logging - INFO - GET /api/tags status=307 duration=0.000s
INFO:     127.0.0.1:60323 - "GET /api/todos HTTP/1.1" 307 Temporary Redirect
INFO:     127.0.0.1:57649 - "GET /api/tags HTTP/1.1" 307 Temporary Redirect
2026-01-25 10:45:28,330 - src.middleware.logging - INFO - GET /api/todos
2026-01-25 10:45:28,330 - src.middleware.logging - INFO - GET /api/todos status=307 duration=0.000s
2026-01-25 10:45:28,330 - src.middleware.logging - INFO - GET /api/tags
INFO:     127.0.0.1:60323 - "GET /api/todos HTTP/1.1" 307 Temporary Redirect
2026-01-25 10:45:28,330 - src.middleware.logging - INFO - GET /api/tags status=307 duration=0.000s
INFO:     127.0.0.1:57649 - "GET /api/tags HTTP/1.1" 307 Temporary Redirect
2026-01-25 10:45:28,344 - src.middleware.logging - INFO - GET /api/todos/
2026-01-25 10:45:28,344 - src.middleware.logging - INFO - GET /api/tags/
2026-01-25 10:45:29,325 - src.middleware.logging - INFO - GET /api/tags/ status=200 duration=0.981s
INFO:     127.0.0.1:57649 - "GET /api/tags/ HTTP/1.1" 200 OK
2026-01-25 10:45:31,252 - src.middleware.logging - INFO - GET /api/tags/
2026-01-25 10:45:32,985 - src.middleware.logging - INFO - GET /api/tags/ status=200 duration=1.732s
INFO:     127.0.0.1:60471 - "GET /api/tags/ HTTP/1.1" 200 OK
2026-01-25 10:45:32,985 - src.middleware.error_handler - ERROR - Unhandled error: 'NONE' is not among the defined enum values. Enum name: priority. Possible values: none, low, medium, high
Traceback (most recent call last):
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\sqlalchemy\sql\sqltypes.py", line 1709, in _object_value_for_elem
    return self._object_lookup[elem]  # type: ignore[return-value]
           ~~~~~~~~~~~~~~~~~~~^^^^^^
KeyError: 'NONE'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\src\middleware\error_handler.py", line 14, in error_handler_middleware
    return await call_next(request)
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\starlette\middleware\base.py", line 168, in call_next  
    raise app_exc from app_exc.__cause__ or app_exc.__context__
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\starlette\middleware\base.py", line 144, in coro       
    await self.app(scope, receive_or_disconnect, send_no_error)
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\starlette\middleware\base.py", line 191, in __call__   
    with recv_stream, send_stream, collapse_excgroups():
  File "C:\Python312\Lib\contextlib.py", line 158, in __exit__
    self.gen.throw(value)
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\starlette\_utils.py", line 85, in collapse_excgroups   
    raise exc
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\starlette\middleware\base.py", line 193, in __call__   
    response = await self.dispatch_func(request, call_next)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\src\middleware\logging.py", line 18, in logging_middleware
    response = await call_next(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\starlette\middleware\base.py", line 168, in call_next  
    raise app_exc from app_exc.__cause__ or app_exc.__context__
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\starlette\middleware\base.py", line 144, in coro       
    await self.app(scope, receive_or_disconnect, send_no_error)
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\starlette\middleware\exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\starlette\_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\fastapi\middleware\asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\starlette\routing.py", line 716, in __call__
    await self.middleware_stack(scope, receive, send)
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\starlette\routing.py", line 736, in app
    await route.handle(scope, receive, send)
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\starlette\routing.py", line 290, in handle
    await self.app(scope, receive, send)
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\fastapi\routing.py", line 115, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\starlette\_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\fastapi\routing.py", line 101, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\fastapi\routing.py", line 355, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\fastapi\routing.py", line 243, in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\src\routers\tasks.py", line 45, in list_tasks
    tasks = task_crud.list_tasks(
            ^^^^^^^^^^^^^^^^^^^^^
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\src\crud\task.py", line 242, in list_tasks
    tasks = session.exec(statement).all()
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\sqlalchemy\engine\result.py", line 1774, in all        
    return self._allrows()
           ^^^^^^^^^^^^^^^
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\sqlalchemy\engine\result.py", line 548, in _allrows    
    rows = self._fetchall_impl()
           ^^^^^^^^^^^^^^^^^^^^^
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\sqlalchemy\engine\result.py", line 1681, in _fetchall_impl
    return self._real_result._fetchall_impl()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\sqlalchemy\engine\result.py", line 2275, in _fetchall_impl
    return list(self.iterator)
           ^^^^^^^^^^^^^^^^^^^
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\sqlalchemy\orm\loading.py", line 220, in chunks        
    fetch = cursor._raw_all_rows()
            ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\sqlalchemy\engine\result.py", line 541, in _raw_all_rows
    return [make_row(row) for row in rows]
            ^^^^^^^^^^^^^
  File "lib/sqlalchemy/cyextension/resultproxy.pyx", line 22, in sqlalchemy.cyextension.resultproxy.BaseRow.__init__
  File "lib/sqlalchemy/cyextension/resultproxy.pyx", line 79, in sqlalchemy.cyextension.resultproxy._apply_processors
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\sqlalchemy\sql\sqltypes.py", line 1829, in process     
    value = self._object_value_for_elem(value)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\sqlalchemy\sql\sqltypes.py", line 1711, in _object_value_for_elem
    raise LookupError(
LookupError: 'NONE' is not among the defined enum values. Enum name: priority. Possible values: none, low, medium, high
INFO:     127.0.0.1:60323 - "GET /api/todos/ HTTP/1.1" 500 Internal Server Error
2026-01-25 10:45:33,012 - src.middleware.logging - INFO - GET /api/todos/
2026-01-25 10:45:34,068 - src.middleware.error_handler - ERROR - Unhandled error: 'NONE' is not among the defined enum values. Enum name: priority. Possible values: none, low, medium, high
Traceback (most recent call last):
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\sqlalchemy\sql\sqltypes.py", line 1709, in _object_value_for_elem
    return self._object_lookup[elem]  # type: ignore[return-value]
           ~~~~~~~~~~~~~~~~~~~^^^^^^
KeyError: 'NONE'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\src\middleware\error_handler.py", line 14, in error_handler_middleware
    return await call_next(request)
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\starlette\middleware\base.py", line 168, in call_next  
    raise app_exc from app_exc.__cause__ or app_exc.__context__
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\starlette\middleware\base.py", line 144, in coro       
    await self.app(scope, receive_or_disconnect, send_no_error)
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\starlette\middleware\base.py", line 191, in __call__   
    with recv_stream, send_stream, collapse_excgroups():
  File "C:\Python312\Lib\contextlib.py", line 158, in __exit__
    self.gen.throw(value)
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\starlette\_utils.py", line 85, in collapse_excgroups   
    raise exc
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\starlette\middleware\base.py", line 193, in __call__   
    response = await self.dispatch_func(request, call_next)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\src\middleware\logging.py", line 18, in logging_middleware
    response = await call_next(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\starlette\middleware\base.py", line 168, in call_next  
    raise app_exc from app_exc.__cause__ or app_exc.__context__
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\starlette\middleware\base.py", line 144, in coro       
    await self.app(scope, receive_or_disconnect, send_no_error)
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\starlette\middleware\exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\starlette\_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\fastapi\middleware\asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\starlette\routing.py", line 716, in __call__
    await self.middleware_stack(scope, receive, send)
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\starlette\routing.py", line 736, in app
    await route.handle(scope, receive, send)
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\starlette\routing.py", line 290, in handle
    await self.app(scope, receive, send)
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\fastapi\routing.py", line 115, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\starlette\_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\fastapi\routing.py", line 101, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\fastapi\routing.py", line 355, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\fastapi\routing.py", line 243, in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\src\routers\tasks.py", line 45, in list_tasks
    tasks = task_crud.list_tasks(
            ^^^^^^^^^^^^^^^^^^^^^
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\src\crud\task.py", line 242, in list_tasks
    tasks = session.exec(statement).all()
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\sqlalchemy\engine\result.py", line 1774, in all        
    return self._allrows()
           ^^^^^^^^^^^^^^^
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\sqlalchemy\engine\result.py", line 548, in _allrows    
    rows = self._fetchall_impl()
           ^^^^^^^^^^^^^^^^^^^^^
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\sqlalchemy\engine\result.py", line 1681, in _fetchall_impl
    return self._real_result._fetchall_impl()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\sqlalchemy\engine\result.py", line 2275, in _fetchall_impl
    return list(self.iterator)
           ^^^^^^^^^^^^^^^^^^^
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\sqlalchemy\orm\loading.py", line 220, in chunks        
    fetch = cursor._raw_all_rows()
            ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\sqlalchemy\engine\result.py", line 541, in _raw_all_rows
    return [make_row(row) for row in rows]
            ^^^^^^^^^^^^^
  File "lib/sqlalchemy/cyextension/resultproxy.pyx", line 22, in sqlalchemy.cyextension.resultproxy.BaseRow.__init__
  File "lib/sqlalchemy/cyextension/resultproxy.pyx", line 79, in sqlalchemy.cyextension.resultproxy._apply_processors
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\sqlalchemy\sql\sqltypes.py", line 1829, in process     
    value = self._object_value_for_elem(value)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\sqlalchemy\sql\sqltypes.py", line 1711, in _object_value_for_elem
    raise LookupError(
LookupError: 'NONE' is not among the defined enum values. Enum name: priority. Possible values: none, low, medium, high
INFO:     127.0.0.1:57649 - "GET /api/todos/ HTTP/1.1" 500 Internal Server Error
