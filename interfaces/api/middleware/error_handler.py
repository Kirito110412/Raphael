from fastapi import Request
from fastapi.responses import JSONResponse

async def error_handling_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as exc:
        return JSONResponse(status_code=500, content={"message": str(exc)})
