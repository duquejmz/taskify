from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4 as uuid
from typing import Optional, Text

app = FastAPI()

tasks = []

# Model
class Task(BaseModel):
    id : str
    title : str
    description : Optional[Text]
    status : str
    tags: list[str]
    date: datetime = datetime.now()
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    
    
class TaskUpdate(BaseModel):
    title : Optional[str]
    description : Optional[Text]
    status : Optional[str]
    tags: Optional[list[str]]
    updated_at: datetime = datetime.now()

@app.get("/")
def read_root():
    return {"Hello": "Hola"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/task/create")
def create_task(task: Task):
    task.id = str(uuid())
    task.created_at = datetime.now()
    task.updated_at = datetime.now()
    tasks.append(task)
    return {"message": "Tarea creada satisfactoriamente", "task": task}

@app.get("/task/{task_id}")
def get_task_by_id(task_id: str):
    task = next((t for t in tasks if t.id == task_id), None)
    if task:
        return task
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

@app.delete("/task/delete/{task_id}")
def delete_task(task_id: str):
    task = next((t for t in tasks if t.id == task_id), None)
    if task:
        tasks.remove(task)
        return {"message": "Tarea eliminada satisfactoriamente"}
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

@app.put("/task/update/{task_id}")
def update_task(task_id: str, task_update: TaskUpdate):
    task = next((t for t in tasks if t.id == task_id), None)
    if task:
        if task_update.title is not None:
            task.title = task_update.title
        if task_update.description is not None:
            task.description = task_update.description
        if task_update.status is not None:
            task.status = task_update.status
        if task_update.tags is not None:
            task.tags = task_update.tags
        task.updated_at = datetime.now()
        return {"message": "Tarea actualizada satisfactoriamente", "task": task}
    raise HTTPException(status_code=404, detail="Tarea no encontrada")