from pydantic import BaseModel


class ExerciseSchema(BaseModel):
    exercise_name: str
    sets: int
    reps: int


class WorkoutSchema(BaseModel):
    workout_name: str
    exercises: list[ExerciseSchema]


class MesoCycleSchema(BaseModel):
    mesocycle_name: str
    workouts: list[WorkoutSchema]
