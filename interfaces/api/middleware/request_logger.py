from fastapi import Request

async def logging_middleware(request: Request, call_next):
    # Stub: log to langfuse
    response = await call_next(request)
    return response
