from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from services.workoutGeneration import generate_workout_plan
from services.mealGeneration import generate_meal_plan

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],  # Frontend URLs
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

class WorkoutResponse(BaseModel):
    workout_plan: str

class MealPlanRequest(BaseModel):
    age: int
    gender: str
    weight: float  # in lbs
    height: float  # in inches
    activity_level: str
    goal: str
    dietary_restrictions: List[str]

class MealPlanCalculations(BaseModel):
    bmr: int
    tdee: int
    target_calories: int

class MealPlanResponse(BaseModel):
    meal_plan: str
    calculations: MealPlanCalculations

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

@app.post("/api/generate-meal-plan", response_model=MealPlanResponse)
async def create_meal_plan(request: MealPlanRequest):
    try:
        # Generate the meal plan
        result = generate_meal_plan(
            age=request.age,
            gender=request.gender,
            weight=request.weight,
            height=request.height,
            activity_level=request.activity_level,
            goal=request.goal,
            dietary_restrictions=request.dietary_restrictions
        )
        
        return MealPlanResponse(
            meal_plan=result["meal_plan"],
            calculations=MealPlanCalculations(**result["calculations"])
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
