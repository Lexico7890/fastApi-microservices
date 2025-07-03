from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI()

tasks = []

id_counter = 1

class Task(BaseModel):
    id: int
    title: str
    description: str
    user_id: int

@app.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://user_service:8000/users/{task.id}")
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="User not found")
        user_data = response.json()

    global id_counter
    task_data = {
        "id": id_counter,
        "title": task.title,
        "description": task.description,
        "user_id": task.user_id,
        "user_name": user_data["name"]
    }
    tasks.append(task_data)
    id_counter += 1
    return task_data

@app.get("/tasks/", response_model=list[Task])
def get_tasks():
    return tasks