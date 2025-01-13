from typing import List, Dict, Optional

def calculate_bmr(weight: float, height: float, age: int, gender: str) -> float:
    """Calculate Basal Metabolic Rate using the Mifflin-St Jeor Equation"""
    if gender.lower() == "male":
        return (10 * weight / 2.205) + (6.25 * height * 2.54) - (5 * age) + 5
    else:
        return (10 * weight / 2.205) + (6.25 * height * 2.54) - (5 * age) - 161

def calculate_tdee(bmr: float, activity_level: str) -> float:
    """Calculate Total Daily Energy Expenditure"""
    activity_multipliers = {
        "sedentary": 1.2,
        "lightly active": 1.375,
        "moderately active": 1.55,
        "very active": 1.725,
        "extra active": 1.9
    }
    return bmr * activity_multipliers.get(activity_level.lower(), 1.2)

def calculate_target_calories(tdee: float, goal: str) -> float:
    """Calculate target calories based on goal"""
    goal_adjustments = {
        "lose weight": -500,
        "maintain weight": 0,
        "gain weight": 500
    }
    return tdee + goal_adjustments.get(goal.lower(), 0)

def generate_meal_plan(
    age: int,
    gender: str,
    weight: float,  # in lbs
    height: float,  # in inches
    activity_level: str,
    goal: str,
    dietary_restrictions: List[str]
) -> Dict:
    """Generate a personalized meal plan based on user parameters."""
    
    # Calculate nutritional needs
    bmr = calculate_bmr(weight, height, age, gender)
    tdee = calculate_tdee(bmr, activity_level)
    target_calories = calculate_target_calories(tdee, goal)
    
    # Create the meal plan
    plan = f"""# Your Personalized Meal Plan

## Nutritional Overview
Your daily caloric needs have been calculated based on your profile:
* Basal Metabolic Rate (BMR): {int(bmr)} calories
* Total Daily Energy Expenditure (TDEE): {int(tdee)} calories
* Target Daily Calories: {int(target_calories)} calories

## Meal Schedule

### Breakfast (25% of daily calories: {int(target_calories * 0.25)} calories)
* Oatmeal with berries and nuts
* Greek yogurt
* Banana
* Green tea or coffee

### Mid-Morning Snack (15% of daily calories: {int(target_calories * 0.15)} calories)
* Apple with almond butter
* Handful of mixed nuts
* Water

### Lunch (30% of daily calories: {int(target_calories * 0.30)} calories)
* Grilled chicken breast
* Brown rice
* Steamed vegetables
* Olive oil dressing
* Water

### Afternoon Snack (10% of daily calories: {int(target_calories * 0.10)} calories)
* Carrot sticks with hummus
* Small handful of trail mix
* Water

### Dinner (20% of daily calories: {int(target_calories * 0.20)} calories)
* Baked salmon
* Sweet potato
* Mixed green salad
* Quinoa
* Water

## Guidelines
* Eat every 3-4 hours
* Drink water throughout the day (aim for 8-10 glasses)
* Include protein with each meal
* Choose whole grains over refined grains
* Include a variety of colorful vegetables
* Listen to your body's hunger and fullness cues

## Meal Prep Tips
* Prepare meals in advance when possible
* Keep healthy snacks readily available
* Use measuring cups/scale initially to learn portion sizes
* Read nutrition labels
* Plan your meals for the week

## Adjustments
* Monitor your progress and adjust portions as needed
* If you're not seeing desired results after 2-3 weeks, adjust calories by 10%
* Stay consistent with your eating schedule
* Get adequate sleep to support your nutrition goals"""

    return {
        "meal_plan": plan,
        "calculations": {
            "bmr": int(bmr),
            "tdee": int(tdee),
            "target_calories": int(target_calories)
        }
    }
