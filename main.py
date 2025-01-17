from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from services.workoutGeneration import generate_workout_plan
from services.mealPlanGeneration import generate_meal_plan

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "https://fit-formula-frontend-yrs4.vercel.app",
        "https://fit-formula-frontend.vercel.app",
        "https://fit-formula-frontend-yrs4-3lzit5boz-samireyes-projects.vercel.app",
        "https://fit-formula-frontend-yrs4-git-feature-614831-samireyes-projects.vercel.app"
    ],
    allow_credentials=True,
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

class MealPlanRequest(BaseModel):
    age: int
    gender: str
    weight: float
    height: float
    activity_level: str
    goal: str
    dietary_restrictions: List[str]

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

@app.api_route("/api/meal-plan", methods=["POST", "OPTIONS"])
async def meal_plan_endpoint(request: Request):
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
        meal_request = MealPlanRequest(**await request.json())
        meal_plan, calculations = generate_meal_plan(
            age=meal_request.age,
            gender=meal_request.gender,
            weight=meal_request.weight,
            height=meal_request.height,
            activity_level=meal_request.activity_level,
            goal=meal_request.goal,
            dietary_restrictions=meal_request.dietary_restrictions
        )
        return JSONResponse(
            content={
                "meal_plan": meal_plan,
                "calculations": calculations
            },
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "*",
            },
        )
    except Exception as e:
        print(f"Error in /api/meal-plan endpoint: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Failed to generate meal plan: {str(e)}"},
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "*",
            },
        )
