import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta

def render_progress_charts(data_manager):
    st.header("Progress Charts")
    
    # Create sample data for the past week
    dates = [(datetime.now() - timedelta(days=x)).date() for x in range(7)]
    dates.reverse()
    
    # Get daily logs for the past week
    daily_totals = []
    for date in dates:
        if 'daily_log' not in st.session_state:
            daily_totals.append({'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0})
            continue
            
        logs = [
            log for log in st.session_state.daily_log 
            if log['timestamp'].date() == date
        ]
        
        totals = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
        for log in logs:
            totals['calories'] += log['calories']
            totals['protein'] += log['protein']
            totals['carbs'] += log['carbs']
            totals['fat'] += log['fat']
            
        daily_totals.append(totals)
    
    # Create calorie trend chart
    fig_calories = go.Figure()
    fig_calories.add_trace(
        go.Scatter(
            x=dates,
            y=[t['calories'] for t in daily_totals],
            mode='lines+markers',
            name='Calories'
        )
    )
    
    fig_calories.update_layout(
        title="Calorie Intake Trend",
        xaxis_title="Date",
        yaxis_title="Calories",
        height=400
    )
    
    st.plotly_chart(fig_calories, use_container_width=True)
    
    # Create macronutrient trend chart
    fig_macros = go.Figure()
    
    fig_macros.add_trace(
        go.Scatter(
            x=dates,
            y=[t['protein'] for t in daily_totals],
            mode='lines+markers',
            name='Protein'
        )
    )
    
    fig_macros.add_trace(
        go.Scatter(
            x=dates,
            y=[t['carbs'] for t in daily_totals],
            mode='lines+markers',
            name='Carbs'
        )
    )
    
    fig_macros.add_trace(
        go.Scatter(
            x=dates,
            y=[t['fat'] for t in daily_totals],
            mode='lines+markers',
            name='Fat'
        )
    )
    
    fig_macros.update_layout(
        title="Macronutrient Trend",
        xaxis_title="Date",
        yaxis_title="Grams",
        height=400
    )
    
    st.plotly_chart(fig_macros, use_container_width=True)
