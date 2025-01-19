from pydantic import BaseModel

class Task(BaseModel):
    task_id: int
    description: str

class TaskCreate(BaseModel):
    description: str