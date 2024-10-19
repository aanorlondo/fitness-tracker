from sqlalchemy import Column, Integer, String, Float, Date
from database import Base


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    type = Column(String)
    series = Column(Integer, nullable=True)
    repetitions = Column(Integer, nullable=True)
    max_series = Column(Integer, nullable=True)
    duration = Column(Integer, nullable=True)
    peak_speed = Column(Float, nullable=True)
    peak_heartbeat = Column(Integer, nullable=True)
    distance = Column(Float, nullable=True)
