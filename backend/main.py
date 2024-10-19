from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Workout
from pydantic import BaseModel

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


class WorkoutData(BaseModel):
    date: str
    type: str  # "pushups", "pullups", "bike"
    series: int = 0
    repetitions: int = 0
    max_series: int = 0
    duration: int = 0
    peak_speed: float = 0.0
    peak_heartbeat: int = 0
    distance: float = 0.0


# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/workouts/")
def add_workout(data: WorkoutData, db: Session = Depends(get_db)):
    workout = Workout(**data.dict())
    db.add(workout)
    db.commit()
    db.refresh(workout)
    return {"message": "Workout added successfully", "workout": workout}


@app.get("/workouts/")
def get_workouts(db: Session = Depends(get_db)):
    return db.query(Workout).all()
