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

    def readtasks(self) -> List[Task]:
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return list(Task(*item) for item in data)

    def writetasks(self, tasks: List[Task]) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([task.dict() for task in tasks], f, ensureascii=False, indent=4)

    def gettasks(self) -> List[Task]:
        return self.readtasks()

    def createtask(self, taskdata: TaskCreate) -> Task:
        tasks = self.readtasks()
        newid = max((task.id for task in tasks), default=0) + 1
        newtask = Task(id=newid, title=taskdata.title, status=taskdata.status)
        tasks.append(newtask)
        self.writetasks(tasks)
        return newtask

    def updatetask(self, taskid: int, taskupdate: TaskUpdate) -> Task:
        tasks = self.readtasks()
        for i, task in enumerate(tasks):
            if task.id == taskid:
                updatedtask = task.copy(update=taskupdate.dict(exclude_unset=True))
                tasks[i] = updatedtask
                self.writetasks(tasks)
                return updatedtask
        raise ValueError("Task not found")

    def deletetask(self, taskid: int) -> None:
        tasks = self.readtasks()
        tasks = [task for task in tasks if task.id != taskid]
        self.writetasks(tasks)