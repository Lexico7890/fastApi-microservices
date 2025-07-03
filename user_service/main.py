from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict
import models, schemas, crud
from database import SessionLocal, engine
import redis
import os
from rq import Queue
from sqlalchemy.orm import Session
from worker import send_welcome_email

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

redis_conn = redis.from_url(os.getenv("REDIS_URL"))
task_queue = Queue(connection=redis_conn)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class User(BaseModel):
    name: str
    email: str

@app.post("/users/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = crud.create_user(db, user)
    task_queue.enqueue(send_welcome_email, new_user.email)
    return new_user

@app.get("/users/{user_id}", response_model=schemas.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user