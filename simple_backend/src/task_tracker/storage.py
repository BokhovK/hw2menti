import json
import os
from typing import List
from models import Task, TaskCreate, TaskUpdate

STORAGEFILE = "tasksdata.json"

class TaskStorage:
    def __init__(self, filepath: str = STORAGEFILE):
        self.filepath = filepath
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump([], f)

    def read_tasks(self) -> List[Task]:
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return list(Task(*item) for item in data)

    def write_tasks(self, tasks: List[Task]) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([task.dict() for task in tasks], f, ensureascii=False, indent=4)

    def gettasks(self) -> List[Task]:
        return self.read_tasks()

    def create_task(self, taskdata: TaskCreate) -> Task:
        tasks = self.read_tasks()
        newid = max((task.id for task in tasks), default=0) + 1
        newtask = Task(id=newid, title=taskdata.title, status=taskdata.status)
        tasks.append(newtask)
        self.writetasks(tasks)
        return newtask

    def update_task(self, taskid: int, taskupdate: TaskUpdate) -> Task:
        tasks = self.readtasks()
        for i, task in enumerate(tasks):
            if task.id == taskid:
                updatedtask = task.copy(update=taskupdate.dict(exclude_unset=True))
                tasks[i] = updatedtask
                self.write_tasks(tasks)
                return updatedtask
        raise ValueError("Task not found")

    def delete_task(self, taskid: int) -> None:
        tasks = self.read_tasks()
        tasks = [task for task in tasks if task.id != taskid]
        self.write_tasks(tasks)