from typing import List, Tuple, Dict

def calculate_bmr(weight: float, height: float, age: int, gender: str) -> float:
    """Calculate Basal Metabolic Rate using the Mifflin-St Jeor Equation"""
    # Convert weight from lbs to kg
    weight_kg = weight * 0.453592
    # Convert height from inches to cm
    height_cm = height * 2.54
    
    if gender.lower() == "male":
        return (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        return (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

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
        "gain weight": 500,
        "build muscle": 300
    }
    return tdee + goal_adjustments.get(goal.lower(), 0)

def generate_meal_plan(
    age: int,
    gender: str,
    weight: float,
    height: float,
    activity_level: str,
    goal: str,
    dietary_restrictions: List[str]
) -> Tuple[str, Dict[str, float]]:
    """Generate a personalized meal plan based on user inputs"""
    
    # Calculate caloric needs
    bmr = calculate_bmr(weight, height, age, gender)
    tdee = calculate_tdee(bmr, activity_level)
    target_calories = calculate_target_calories(tdee, goal)
    
    # Format dietary restrictions
    restrictions_text = ", ".join(dietary_restrictions) if dietary_restrictions else "None"
    
    # Generate the meal plan
    meal_plan = f"""# Your Personalized Meal Plan

## Daily Nutritional Targets
- **Target Calories:** {int(target_calories)} calories
- **Dietary Restrictions:** {restrictions_text}

## Meal Schedule

### Breakfast (25% of daily calories: {int(target_calories * 0.25)} cal)
- Oatmeal with berries and nuts
- Greek yogurt
- Banana

### Morning Snack (15% of daily calories: {int(target_calories * 0.15)} cal)
- Apple with almond butter
- Handful of mixed nuts

### Lunch (30% of daily calories: {int(target_calories * 0.30)} cal)
- Grilled chicken breast
- Quinoa
- Steamed vegetables
- Olive oil dressing

### Afternoon Snack (10% of daily calories: {int(target_calories * 0.10)} cal)
- Carrot sticks with hummus
- String cheese

### Dinner (20% of daily calories: {int(target_calories * 0.20)} cal)
- Baked salmon
- Sweet potato
- Roasted broccoli
- Mixed green salad

## Guidelines
1. Drink at least 8 glasses of water daily
2. Eat every 3-4 hours
3. Include protein with each meal
4. Focus on whole, unprocessed foods
5. Adjust portions to meet caloric goals

## Notes
- This meal plan is a template - adjust portions to meet your caloric needs
- Listen to your body and adjust meal timing as needed
- Consider tracking your meals using a food diary
"""

    calculations = {
        "bmr": round(bmr, 2),
        "tdee": round(tdee, 2),
        "target_calories": round(target_calories, 2)
    }
    
    return meal_plan, calculations
