from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    name: str = Field(max_length=128)
    description: str | None = Field(None)
    

class TaskOut(TaskCreate):
    id: int
    user_id: int
    status: bool
    priority: int
    category: str
