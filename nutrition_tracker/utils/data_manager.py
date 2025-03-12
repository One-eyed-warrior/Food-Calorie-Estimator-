import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

class DataManager:
    def __init__(self):
        self.food_db = pd.read_csv('data/food_database.csv')
        
    def get_food_items(self):
        """Return list of available food items"""
        return self.food_db['food_name'].tolist()
        
    def get_food_info(self, food_name):
        """Get nutritional information for a specific food"""
        food = self.food_db[self.food_db['food_name'] == food_name].iloc[0]
        return {
            'serving_size': food['serving_size'],
            'calories': food['calories'],
            'protein': food['protein'],
            'carbs': food['carbs'],
            'fat': food['fat']
        }
        
    def log_meal(self, food_name, portions):
        """Log a meal to the session state"""
        if 'daily_log' not in st.session_state:
            st.session_state.daily_log = []
            
        food_info = self.get_food_info(food_name)
        meal_entry = {
            'food_name': food_name,
            'portions': portions,
            'calories': food_info['calories'] * portions,
            'protein': food_info['protein'] * portions,
            'carbs': food_info['carbs'] * portions,
            'fat': food_info['fat'] * portions,
            'timestamp': datetime.now()
        }
        
        st.session_state.daily_log.append(meal_entry)
        
    def get_daily_totals(self):
        """Calculate total nutrition for the day"""
        if 'daily_log' not in st.session_state:
            return {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
            
        today = datetime.now().date()
        today_logs = [
            log for log in st.session_state.daily_log 
            if log['timestamp'].date() == today
        ]
        
        totals = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
        for log in today_logs:
            totals['calories'] += log['calories']
            totals['protein'] += log['protein']
            totals['carbs'] += log['carbs']
            totals['fat'] += log['fat']
            
        return totals
