from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from services.workoutGeneration import generate_workout_plan

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
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

@app.get("/api/test")
async def test_endpoint():
    return {"message": "API is working!", "status": "ok"}

@app.api_route("/api/workout", methods=["POST", "OPTIONS"])
async def workout_endpoint(request: Request):
    if request.method == "OPTIONS":
        return JSONResponse(
            content={"message": "OK"},
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "*",
            },
        )
    
    try:
        workout_request = WorkoutRequest(**await request.json())
        workout_plan = generate_workout_plan(
            fitness_level=workout_request.fitness_level,
            equipment_available=workout_request.available_equipment,
            goal=workout_request.goals,
            time_available=workout_request.time_per_session,
            sessions_per_week=workout_request.sessions_per_week,
            medical_conditions=workout_request.medical_conditions
        )
        return JSONResponse(
            content={"workout_plan": workout_plan},
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "*",
            },
        )
    except Exception as e:
        print(f"Error in /api/workout endpoint: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Failed to generate workout plan: {str(e)}"},
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "*",
            },
        )
