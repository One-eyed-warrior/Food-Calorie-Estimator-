class NutritionCalculator:
    @staticmethod
    def calculate_daily_needs(weight_kg, height_cm, age, gender, activity_level):
        """Calculate daily caloric needs using Harris-Benedict equation"""
        if gender.lower() == 'male':
            bmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)

        activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very active': 1.9
        }
        
        daily_calories = bmr * activity_multipliers.get(activity_level.lower(), 1.2)
        
        return {
            'calories': round(daily_calories),
            'protein': round(daily_calories * 0.3 / 4),  # 30% of calories from protein
            'carbs': round(daily_calories * 0.45 / 4),   # 45% of calories from carbs
            'fat': round(daily_calories * 0.25 / 9)      # 25% of calories from fat
        }

    @staticmethod
    def calculate_meal_nutrients(food_items):
        """Calculate total nutrients for multiple food items"""
        total = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
        
        for item in food_items:
            total['calories'] += item['calories']
            total['protein'] += item['protein']
            total['carbs'] += item['carbs']
            total['fat'] += item['fat']
            
        return total
