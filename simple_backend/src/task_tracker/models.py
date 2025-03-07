from pydantic import BaseModel
from typing import Optional

class Task(BaseModel):
    id: int
    title: str
    status: str

class TaskCreate(BaseModel):
    title: str
    status: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None 

