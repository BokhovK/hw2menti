from fastapi import FastAPI, HTTPException
from models import Task, TaskCreate, TaskUpdate
from storage import TaskStorage
from clients import LLMClient
from dotenv import load_dotenv
import os

app = FastAPI(title="Task Tracker API")

storage = TaskStorage()


LLM_API_KEY = os.getenv("LLM_API_KEY")
print(LLM_API_KEY)

@app.get("/tasks", response_model=list[Task])
def get_tasks():
    """
    Возвращаем список всех задач
    """
    return storage.get_tasks()

@app.post("/tasks", response_model=Task)
def create_task(task_create: TaskCreate):
    """
    Создаём новую задачу. При создании отправляем текст задачи в LLM для получения способов решения.
    И если LLM возвращает пояснение, добавляем его в название задачи (или можно расширить модель).
    """
    explanation = llm_client.get_task_solution(task_create.title)
    # Например, добавляем пояснение в конец названия
    task_create.title = f"{task_create.title}\nРешение: {explanation}"
    new_task = storage.create_task(task_create)
    return new_task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate):
    """
    Обновляем информацию о задаче
    """
    try:
        updated = storage.updatetask(task_id, task_update)
        return updated
    except ValueError:
        raise HTTPException(statuscode=404, detail="Task not found")

@app.delete("/tasks/{taskid}")
def deletetask(taskid: int):
    """
    Удаляем задачу
    """
    try:
        storage.deletetask(taskid)
        return {"detail": "Task deleted"}
    except Exception as e:
        raise HTTPException(statuscode=400, detail=str(e))