from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class TaskRequest(BaseModel):
    input: str
    modality: str
    priority: int = 0

@router.post("/task")
def submit_task(request: TaskRequest):
    return {"status": "accepted", "task_id": "stub_id", "input": request.input}

@router.get("/task/{task_id}/status")
def get_task_status(task_id: str):
    return {"status": "running", "progress_pct": 50, "eta_seconds": 30}

@router.get("/task/{task_id}/result")
def get_task_result(task_id: str):
    return {"output": "Stub output", "confidence": 0.9, "sources": []}
