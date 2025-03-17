import React, { useState } from 'react';
import { Utensils } from 'lucide-react';
import { AddFoodForm } from './components/AddFoodForm';
import { NutritionSummary } from './components/NutritionSummary';
import { FoodList } from './components/FoodList';
import { CameraFoodDetection } from './components/CameraFoodDetection';
import { FoodItem } from './types';

// Common food nutrition data (approximate values)
const foodDatabase: Record<string, { calories: number; protein: number; carbs: number; fat: number }> = {
  banana: { calories: 105, protein: 1.3, carbs: 27, fat: 0.3 },
  apple: { calories: 95, protein: 0.5, carbs: 25, fat: 0.3 },
  orange: { calories: 62, protein: 1.2, carbs: 15, fat: 0.2 },
  carrot: { calories: 41, protein: 0.9, carbs: 10, fat: 0.2 },
  broccoli: { calories: 55, protein: 3.7, carbs: 11, fat: 0.6 },
  sandwich: { calories: 300, protein: 15, carbs: 35, fat: 12 },
  pizza: { calories: 285, protein: 12, carbs: 36, fat: 10 },
  donut: { calories: 250, protein: 4, carbs: 30, fat: 14 },
  cake: { calories: 350, protein: 5, carbs: 50, fat: 15 }
};

function App() {
  const [foods, setFoods] = useState<FoodItem[]>([]);

  const handleAddFood = (food: FoodItem) => {
    setFoods([...foods, food]);
  };

  const handleDeleteFood = (id: string) => {
    setFoods(foods.filter(food => food.id !== id));
  };

  const handleFoodDetected = (foodName: string) => {
    const detectedFood = foodDatabase[foodName.toLowerCase()];
    if (detectedFood) {
      const newFood: FoodItem = {
        id: Date.now().toString(),
        name: foodName,
        calories: detectedFood.calories,
        protein: detectedFood.protein,
        carbs: detectedFood.carbs,
        fat: detectedFood.fat,
        date: new Date()
      };
      handleAddFood(newFood);
    }
  };

  const nutritionSummary = foods.reduce(
    (acc, food) => ({
      totalCalories: acc.totalCalories + food.calories,
      totalProtein: acc.totalProtein + food.protein,
      totalCarbs: acc.totalCarbs + food.carbs,
      totalFat: acc.totalFat + food.fat,
    }),
    { totalCalories: 0, totalProtein: 0, totalCarbs: 0, totalFat: 0 }
  );

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex items-center justify-center mb-8">
          <Utensils className="w-8 h-8 text-blue-600 mr-3" />
          <h1 className="text-3xl font-bold text-gray-900">Calorie Tracker</h1>
        </div>

        <div className="space-y-8">
          <NutritionSummary summary={nutritionSummary} />
          
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-1 space-y-8">
              <CameraFoodDetection onFoodDetected={handleFoodDetected} />
              <AddFoodForm onAddFood={handleAddFood} />
            </div>
            
            <div className="lg:col-span-2">
              <div className="bg-white p-6 rounded-lg shadow-md">
                <h2 className="text-xl font-semibold mb-4">Today's Food Log</h2>
                <FoodList foods={foods} onDeleteFood={handleDeleteFood} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;