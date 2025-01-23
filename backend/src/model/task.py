from pydantic import BaseModel, Field

class Task(BaseModel):
    task_id: int
    task: str

class TaskCreate(BaseModel):
    task: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="The task to be completed",
        example="Buy groceries"
    )