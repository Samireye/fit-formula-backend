from typing import List, Optional, Dict

def get_exercises_by_equipment(equipment: List[str]) -> Dict[str, List[Dict[str, str]]]:
    """Get appropriate exercises based on available equipment"""
    # Normalize equipment names
    normalized_equipment = [e.replace('_', ' ').title() for e in equipment]
    
    exercises = {
        "bodyweight": {
            "upper_push": [
                {"name": "Push-ups", "sets": "3-4", "reps": "10-15", "rest": "90 seconds",
                 "cue": "Keep your core tight and body in a straight line"},
                {"name": "Pike Push-ups", "sets": "3", "reps": "8-12", "rest": "90 seconds",
                 "cue": "Keep elbows close to body, focus on shoulder engagement"}
            ],
            "upper_pull": [
                {"name": "Inverted Rows", "sets": "3", "reps": "8-12", "rest": "90 seconds",
                 "cue": "Keep your core engaged and pull your chest to the bar"},
                {"name": "Superman Holds", "sets": "3", "reps": "20-30 seconds", "rest": "60 seconds",
                 "cue": "Squeeze your back muscles and hold"}
            ],
            "legs": [
                {"name": "Bodyweight Squats", "sets": "4", "reps": "15-20", "rest": "90 seconds",
                 "cue": "Keep chest up and push through your heels"},
                {"name": "Walking Lunges", "sets": "3", "reps": "12 steps each leg", "rest": "90 seconds",
                 "cue": "Take controlled steps and maintain good posture"}
            ],
            "core": [
                {"name": "Plank", "sets": "3", "reps": "30-45 seconds", "rest": "60 seconds",
                 "cue": "Keep your body in a straight line"},
                {"name": "Mountain Climbers", "sets": "3", "reps": "20 each leg", "rest": "60 seconds",
                 "cue": "Maintain a steady pace and keep hips level"}
            ]
        },
        "barbell": {
            "upper_push": [
                {"name": "Bench Press", "sets": "4", "reps": "8-10", "rest": "2 minutes",
                 "cue": "Keep your feet planted and maintain a slight arch in your back"},
                {"name": "Overhead Press", "sets": "3", "reps": "8-12", "rest": "90 seconds",
                 "cue": "Keep your core tight and avoid excessive back arch"}
            ],
            "upper_pull": [
                {"name": "Barbell Rows", "sets": "4", "reps": "8-10", "rest": "90 seconds",
                 "cue": "Keep your back straight and pull to your lower chest"},
                {"name": "Pendlay Rows", "sets": "3", "reps": "8-12", "rest": "90 seconds",
                 "cue": "Pull explosively to your chest, control the descent"}
            ],
            "legs": [
                {"name": "Barbell Squats", "sets": "4", "reps": "6-8", "rest": "2-3 minutes",
                 "cue": "Keep chest up and push through your heels"},
                {"name": "Romanian Deadlifts", "sets": "4", "reps": "8-10", "rest": "2 minutes",
                 "cue": "Hinge at your hips and maintain a neutral spine"}
            ]
        },
        "resistance_bands": {
            "upper_push": [
                {"name": "Band Chest Press", "sets": "3", "reps": "12-15", "rest": "60 seconds",
                 "cue": "Keep core engaged and maintain controlled movements"},
                {"name": "Banded Overhead Press", "sets": "3", "reps": "12-15", "rest": "60 seconds",
                 "cue": "Press band overhead while maintaining core stability"}
            ],
            "upper_pull": [
                {"name": "Band Pull-aparts", "sets": "3", "reps": "12-15", "rest": "60 seconds",
                 "cue": "Keep shoulders down and focus on squeezing shoulder blades"},
                {"name": "Banded Face Pulls", "sets": "3", "reps": "15-20", "rest": "60 seconds",
                 "cue": "Pull towards your face with high elbows, squeeze at the end"}
            ],
            "legs": [
                {"name": "Banded Squats", "sets": "3", "reps": "12-15", "rest": "90 seconds",
                 "cue": "Place band above knees, push knees out against band"},
                {"name": "Banded Good Mornings", "sets": "3", "reps": "12-15", "rest": "90 seconds",
                 "cue": "Hinge at hips, maintain tension in the band"}
            ]
        }
    }
    
    available_exercises = {
        "upper_push": [],
        "upper_pull": [],
        "legs": [],
        "core": []
    }
    
    # Only include bodyweight exercises if specifically selected or if no other equipment is available
    if "Bodyweight Only" in normalized_equipment:
        for category in available_exercises:
            if category in exercises["bodyweight"]:
                available_exercises[category].extend(exercises["bodyweight"][category])
    
    # Add equipment-specific exercises
    if any(e in normalized_equipment for e in ["Barbell", "Dumbbells"]):
        for category in available_exercises:
            if category in exercises["barbell"]:
                available_exercises[category].extend(exercises["barbell"][category])
    
    if "Resistance Bands" in normalized_equipment:
        for category in available_exercises:
            if category in exercises["resistance_bands"]:
                available_exercises[category].extend(exercises["resistance_bands"][category])
    
    # If no exercises were added (because no equipment was selected), include bodyweight as fallback
    if all(len(exercises) == 0 for exercises in available_exercises.values()):
        for category in available_exercises:
            if category in exercises["bodyweight"]:
                available_exercises[category].extend(exercises["bodyweight"][category])
    
    return available_exercises

def generate_workout_splits(sessions_per_week: int) -> List[str]:
    """Generate appropriate workout splits based on number of sessions per week"""
    if sessions_per_week == 3:
        return ["Full Body", "Rest", "Full Body", "Rest", "Full Body"]
    elif sessions_per_week == 4:
        return ["Upper Body", "Lower Body", "Rest", "Upper Body", "Lower Body"]
    elif sessions_per_week == 5:
        return ["Push", "Pull", "Legs", "Upper Body", "Lower Body"]
    elif sessions_per_week == 6:
        return ["Push", "Pull", "Legs", "Push", "Pull", "Legs"]
    else:
        return ["Full Body"] * sessions_per_week

def get_workout_exercises(workout_type: str, available_exercises: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    """Get exercises for a specific workout type"""
    exercises = []
    
    if workout_type == "Full Body":
        # For full body, get one exercise from each category if available
        for category in ["upper_push", "upper_pull", "legs"]:
            if category in available_exercises and available_exercises[category]:
                exercises.append(available_exercises[category][0])
    
    elif workout_type == "Upper Body" or workout_type == "Push":
        # For upper body, get all upper push exercises and some pull if it's upper body day
        if "upper_push" in available_exercises and available_exercises["upper_push"]:
            exercises.extend(available_exercises["upper_push"])
        if workout_type == "Upper Body" and "upper_pull" in available_exercises and available_exercises["upper_pull"]:
            exercises.extend(available_exercises["upper_pull"])
    
    elif workout_type == "Lower Body" or workout_type == "Legs":
        # For lower body, get all leg exercises
        if "legs" in available_exercises and available_exercises["legs"]:
            exercises.extend(available_exercises["legs"])
    
    elif workout_type == "Pull":
        # For pull day, get all pull exercises
        if "upper_pull" in available_exercises and available_exercises["upper_pull"]:
            exercises.extend(available_exercises["upper_pull"])
    
    # If no exercises were selected (which shouldn't happen), add a warning message
    if not exercises:
        exercises.append({
            "name": "No suitable exercises found",
            "sets": "N/A",
            "reps": "N/A",
            "rest": "N/A",
            "cue": "Please select different equipment or contact support"
        })
    
    return exercises

def generate_workout_plan(
    fitness_level: str,
    equipment_available: List[str],
    goal: str,
    time_available: int,
    sessions_per_week: int,
    medical_conditions: Optional[str] = None
) -> str:
    """Generate a personalized workout plan based on user parameters."""
    
    try:
        # Get appropriate exercises based on equipment
        available_exercises = get_exercises_by_equipment(equipment_available)
        
        # Get workout split based on sessions per week
        workout_split = generate_workout_splits(sessions_per_week)
        
        # Create workout plan introduction
        plan = f"""# Your Personalized {goal} Workout Plan

## Weekly Overview
This {sessions_per_week}-day workout plan is designed for a {fitness_level}-level individual focusing on {goal.lower()}. Each session lasts approximately {time_available} minutes and includes warm-up, main exercises, and cool-down stretches. Rest days are essential for muscle recovery and growth.

"""

        # Add each day's workout
        for day_num, workout_type in enumerate(workout_split, 1):
            if workout_type == "Rest":
                plan += f"""## Day {day_num} - Rest and Recovery
* Light stretching
* Foam rolling
* Walking or light cardio (optional)
* Focus on proper nutrition and hydration

"""
            else:
                plan += f"""## Day {day_num} - {workout_type}

### Warm-up (10-15 minutes)
* 5 minutes of light cardio (jumping jacks, jump rope, or jogging)
* Dynamic stretches for major muscle groups
* Joint mobility exercises

### Main Exercises
"""
                # Get exercises for this workout type
                exercises = get_workout_exercises(workout_type, available_exercises)
                
                for exercise in exercises:
                    plan += f"""* {exercise['name']}: {exercise['sets']} sets × {exercise['reps']}, {exercise['rest']}
  - Form Cue: {exercise['cue']}
"""

                plan += """
### Cool-down (5-10 minutes)
* Static stretching for worked muscle groups
* Light walking to normalize heart rate
* Stay hydrated

"""

        # Add general guidelines
        plan += """## General Guidelines
* Always warm up properly before each workout
* Focus on proper form over reps
* Stay hydrated throughout your workouts
* Get adequate sleep (7-9 hours) to support recovery
* If you experience sharp pain (not normal muscle fatigue), stop and consult a professional
* Adjust intensity based on your recovery and progression

## Progression Tips
* Start with the lower end of the rep ranges
* When you can complete all sets at the max reps with good form, increase difficulty:
  - For bodyweight exercises: modify to a harder variation
  - For weighted exercises: increase weight by 2-5%
* Listen to your body and progress at your own pace
* Rest between sets is crucial - use the recommended rest periods"""

        return plan
        
    except Exception as e:
        print(f"Error generating workout plan: {str(e)}")
        raise Exception(f"Failed to generate workout plan: {str(e)}")
