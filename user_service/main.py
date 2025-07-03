from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

fake_db: Dict[int, dict] = {}
id_counter = 1

class User(BaseModel):
    name: str
    email: str

@app.post("/users/", response_model=User)
async def create_user(user: User):
    global id_counter
    if id_counter in fake_db:
        raise HTTPException(status_code=400, detail="User already exists")
    
    user_data = user.model_dump()
    user_data["id"] = id_counter
    id_counter += 1
    fake_db[id_counter] = user_data
    return user_data

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    return fake_db[user_id]