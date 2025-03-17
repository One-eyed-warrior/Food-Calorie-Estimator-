import React from 'react';
import { format } from 'date-fns';
import { Trash2 } from 'lucide-react';
import { FoodItem } from '../types';

interface FoodListProps {
  foods: FoodItem[];
  onDeleteFood: (id: string) => void;
}

export function FoodList({ foods, onDeleteFood }: FoodListProps) {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Time</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Food</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Calories</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Protein</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Carbs</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fat</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {foods.map((food) => (
              <tr key={food.id}>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {format(food.date, 'HH:mm')}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{food.name}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{food.calories}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{food.protein}g</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{food.carbs}g</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{food.fat}g</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  <button
                    onClick={() => onDeleteFood(food.id)}
                    className="text-red-600 hover:text-red-900"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}