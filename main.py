from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from services.workoutGeneration import generate_workout_plan

app = FastAPI()

# Configure CORS with more specific settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # Changed to False since we're using "*" for origins
    allow_methods=["GET", "POST", "OPTIONS"],  # Explicitly list allowed methods
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,  # Cache preflight requests for 10 minutes
)

class WorkoutRequest(BaseModel):
    fitness_level: str
    available_equipment: List[str]
    goals: str
    time_per_session: int
    sessions_per_week: int
    medical_conditions: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "Welcome to FitFormula API"}

@app.options("/api/workout")
async def workout_options():
    return {"message": "OK"}

@app.post("/api/workout")
async def generate_workout(request: WorkoutRequest):
    try:
        workout_plan = generate_workout_plan(
            fitness_level=request.fitness_level,
            equipment_available=request.available_equipment,
            goal=request.goals,
            time_available=request.time_per_session,
            sessions_per_week=request.sessions_per_week,
            medical_conditions=request.medical_conditions
        )
        return {"workout_plan": workout_plan}
    except Exception as e:
        print(f"Error in /api/workout endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate workout plan: {str(e)}"
        )
