from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from interfaces.api.routes import task_routes, health_routes
from interfaces.api.middleware.auth import auth_middleware
from interfaces.api.middleware.rate_limiter import rate_limit_middleware
from interfaces.api.middleware.request_logger import logging_middleware
from interfaces.api.middleware.error_handler import error_handling_middleware

app = FastAPI(title="MyAI API Daemon")

# Add middleware (order matters: error handler first, then logger, etc.)
app.add_middleware(BaseHTTPMiddleware, dispatch=error_handling_middleware)
app.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)
app.add_middleware(BaseHTTPMiddleware, dispatch=rate_limit_middleware)
app.add_middleware(BaseHTTPMiddleware, dispatch=auth_middleware)

# Include routes
app.include_router(task_routes.router)
app.include_router(health_routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
