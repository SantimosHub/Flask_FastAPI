from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import pandas as pd
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

tasks = []


class Task(BaseModel):
    id: int
    title: str
    description: str
    status: Optional[bool] = False


@app.get("/tasks", response_class=HTMLResponse)
async def show_tasks(request: Request):
    tasks_list = pd.DataFrame([vars(task) for task in tasks]).to_html(index=False)
    return templates.TemplateResponse("tasks.html", {"request": request, "tasks_list": tasks_list})


@app.get("/tasks/{task_id}", response_class=HTMLResponse)
async def show_task(request: Request, task_id: int):
    task = pd.DataFrame([vars(t) for t in tasks if t.id == task_id]).to_html(index=False)
    return templates.TemplateResponse("tasks.html", {"request": request, "task": task})


@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    task_id = len(tasks) + 1
    task.id = task_id
    tasks.append(task)
    return task


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    for i, new_task in enumerate(tasks):
        if new_task.id == task_id:
            task.id = task_id
            tasks[i] = task
            return task
    else:
        raise HTTPException(status_code=404, detail="Задачи с таким ID не существует")


@app.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: int):
    for i, remove_task in enumerate(tasks):
        if remove_task.id == task_id:
            return tasks.pop(i)
    else:
        raise HTTPException(status_code=404, detail="Задачи с таким ID не существует")


if __name__ == '__main__':
    uvicorn.run(app)
