import json
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
from cloudflare_ai import CloudflareAI 

app = FastAPI(title="Task Manager API")
ai = CloudflareAI(api_url="https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/text",
                  api_key=os.getenv("bvrlI_M2mfc-D1sMvdqucoHwUb4nkgd5K_ZMqdz-"))  

TASKS_FILE = "tasks.json"
API_URL = 'https:// 67c7475ac19eb8753e794b78.mockapi.io/api/v1/tasks'

class Task(BaseModel):
    description: str
    done: bool = False


class TaskUpdate(BaseModel):
    description: Optional[str] = None
    done: Optional[bool] = None


class TaskManager:
    def __init__(self, filepath: str = TASKS_FILE):
        self.filepath = filepath
        self.tasks: Dict[str, dict] = {}
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    self.tasks = json.load(f)
            except json.JSONDecodeError:
                print("Ошибка: не удалось разобрать JSON из файла. Будет использовано пустое хранилище.")
                self.tasks = {}
        else:
            self.tasks = {}

    def save_tasks(self):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=4)

    def get_all_tasks(self):
        return self.tasks

    def get_task(self, task_id: str):
        return self.tasks.get(task_id)

    def add_task(self, task_id: str, task: Task):
        if task_id in self.tasks:
            raise ValueError("Задача с таким идентификатором уже существует.")
        self.tasks[task_id] = task.dict()
        self.save_tasks()

    def update_task(self, task_id: str, task_data: TaskUpdate):
        if task_id not in self.tasks:
            raise KeyError("Задача не найдена.")
        if task_data.description is not None:
            self.tasks[task_id]['description'] = task_data.description
        if task_data.done is not None:
            self.tasks[task_id]['done'] = task_data.done
        self.save_tasks()

    def remove_task(self, task_id: str):
        if task_id not in self.tasks:
            raise KeyError("Задача не найдена.")
        del self.tasks[task_id]
        self.save_tasks()



task_manager = TaskManager()


@app.get("/tasks", response_model=Dict[str, Task])
def read_tasks():
    return task_manager.get_all_tasks()


@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: str):
    task = task_manager.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task


@app.post("/tasks/{task_id}", response_model=Task)
def create_task(task_id: str, task: Task):
    try:
        task_manager.add_task(task_id, task)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, task_data: TaskUpdate):
    try:
        task_manager.update_task(task_id, task_data)
        updated_task = task_manager.get_task(task_id)
        return updated_task
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    try:
        task_manager.remove_task(task_id)
        return {"detail": "Задача удалена"}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))