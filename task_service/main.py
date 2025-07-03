from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

tasks = []

id_counter = 1

class Task(BaseModel):
    id: int
    title: str
    description: str = None

@app.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    