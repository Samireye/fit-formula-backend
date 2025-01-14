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

    # Define meal options based on dietary preferences
    meal_options = {
        "carnivore": {
            "breakfast": [
                "Eggs and bacon",
                "Ground beef with eggs",
                "Steak and eggs",
                "Pork chops",
                "Beef liver"
            ],
            "snacks": [
                "Beef jerky",
                "Hard-boiled eggs",
                "Pork rinds",
                "Bone broth"
            ],
            "lunch_dinner": [
                "Ribeye steak",
                "Ground beef patties",
                "Chicken thighs",
                "Lamb chops",
                "Turkey legs",
                "Beef brisket"
            ]
        },
        "pescatarian": {
            "breakfast": [
                "Greek yogurt with berries",
                "Smoked salmon with eggs",
                "Tuna avocado toast",
                "Sardines on whole grain bread"
            ],
            "snacks": [
                "Mixed nuts",
                "Seaweed snacks",
                "Cottage cheese",
                "Canned sardines"
            ],
            "lunch_dinner": [
                "Grilled salmon",
                "Baked cod",
                "Shrimp stir-fry",
                "Tuna steak",
                "Sea bass with vegetables",
                "Mussels in garlic sauce"
            ]
        }
    }

    # Select appropriate meal template based on dietary preferences
    if "carnivore" in dietary_restrictions:
        meals = meal_options["carnivore"]
        meal_plan = f"""# Your Personalized Carnivore Meal Plan

## Daily Nutritional Targets
- **Target Calories:** {int(target_calories)} calories
- **Dietary Preferences:** {restrictions_text}

## Meal Schedule

### Breakfast (30% of daily calories: {int(target_calories * 0.30)} cal)
- {meals["breakfast"][0]}
- {meals["breakfast"][1]}

### Morning Snack (10% of daily calories: {int(target_calories * 0.10)} cal)
- {meals["snacks"][0]}
- {meals["snacks"][1]}

### Lunch (30% of daily calories: {int(target_calories * 0.30)} cal)
- {meals["lunch_dinner"][0]}
- {meals["lunch_dinner"][1]}

### Afternoon Snack (10% of daily calories: {int(target_calories * 0.10)} cal)
- {meals["snacks"][2]}
- {meals["snacks"][3]}

### Dinner (20% of daily calories: {int(target_calories * 0.20)} cal)
- {meals["lunch_dinner"][2]}
- {meals["lunch_dinner"][3]}

## Guidelines
1. Focus on fatty cuts of meat for energy
2. Include organ meats for nutrients
3. Consider adding bone broth for minerals
4. Salt to taste
5. Eat when hungry, stop when full

## Notes
- This is a zero-carb, animal-based meal plan
- Adjust portions to meet your caloric needs
- Listen to your body and adjust meal timing as needed
"""
    elif "pescatarian" in dietary_restrictions:
        meals = meal_options["pescatarian"]
        meal_plan = f"""# Your Personalized Pescatarian Meal Plan

## Daily Nutritional Targets
- **Target Calories:** {int(target_calories)} calories
- **Dietary Preferences:** {restrictions_text}

## Meal Schedule

### Breakfast (25% of daily calories: {int(target_calories * 0.25)} cal)
- {meals["breakfast"][0]}
- {meals["breakfast"][1]}

### Morning Snack (15% of daily calories: {int(target_calories * 0.15)} cal)
- {meals["snacks"][0]}
- {meals["snacks"][1]}

### Lunch (30% of daily calories: {int(target_calories * 0.30)} cal)
- {meals["lunch_dinner"][0]}
- Mixed green salad
- Quinoa or brown rice

### Afternoon Snack (10% of daily calories: {int(target_calories * 0.10)} cal)
- {meals["snacks"][2]}
- Fresh fruit

### Dinner (20% of daily calories: {int(target_calories * 0.20)} cal)
- {meals["lunch_dinner"][1]}
- Steamed vegetables
- Sweet potato or whole grain

## Guidelines
1. Include a variety of fish for omega-3s
2. Eat plenty of plant-based proteins
3. Include whole grains and legumes
4. Focus on healthy fats from fish, nuts, and oils
5. Aim for 2-3 servings of fish per day

## Notes
- Rotate between different types of fish for nutrient variety
- Consider algae supplements for additional omega-3s
- Include plant-based protein sources like legumes and quinoa
"""
    else:
        # Original meal plan for other dietary preferences
        meal_plan = f"""# Your Personalized Meal Plan

## Daily Nutritional Targets
- **Target Calories:** {int(target_calories)} calories
- **Dietary Preferences:** {restrictions_text}

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
