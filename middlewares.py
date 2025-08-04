from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
import time


class SimpleMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print("Before request")
        response = await call_next(request)
        print("After response")
        return response

class TimerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        duration = time.time() - start_time
        print(f"Time taken : {duration:.4f} seconds")
        
        return response