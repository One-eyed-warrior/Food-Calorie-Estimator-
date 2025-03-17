import React from 'react';
import { Activity, Flame, Wheat as Meat, Heading as Bread } from 'lucide-react';
import { NutritionSummary as NutritionSummaryType } from '../types';

interface NutritionSummaryProps {
  summary: NutritionSummaryType;
}

export function NutritionSummary({ summary }: NutritionSummaryProps) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div className="bg-white p-4 rounded-lg shadow-md">
        <div className="flex items-center">
          <Flame className="w-5 h-5 text-red-500 mr-2" />
          <h3 className="text-sm font-medium text-gray-700">Calories</h3>
        </div>
        <p className="mt-2 text-2xl font-semibold">{summary.totalCalories}</p>
      </div>
      <div className="bg-white p-4 rounded-lg shadow-md">
        <div className="flex items-center">
          <Meat className="w-5 h-5 text-purple-500 mr-2" />
          <h3 className="text-sm font-medium text-gray-700">Protein</h3>
        </div>
        <p className="mt-2 text-2xl font-semibold">{summary.totalProtein}g</p>
      </div>
      <div className="bg-white p-4 rounded-lg shadow-md">
        <div className="flex items-center">
          <Bread className="w-5 h-5 text-yellow-500 mr-2" />
          <h3 className="text-sm font-medium text-gray-700">Carbs</h3>
        </div>
        <p className="mt-2 text-2xl font-semibold">{summary.totalCarbs}g</p>
      </div>
      <div className="bg-white p-4 rounded-lg shadow-md">
        <div className="flex items-center">
          <Activity className="w-5 h-5 text-green-500 mr-2" />
          <h3 className="text-sm font-medium text-gray-700">Fat</h3>
        </div>
        <p className="mt-2 text-2xl font-semibold">{summary.totalFat}g</p>
      </div>
    </div>
  );
}