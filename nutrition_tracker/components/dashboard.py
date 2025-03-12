import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

def render_dashboard(data_manager):
    st.header("Daily Nutrition Dashboard")
    
    # Get daily totals and goals
    daily_totals = data_manager.get_daily_totals()
    daily_goals = st.session_state.get('daily_goals', {
        'calories': 2000,
        'protein': 150,
        'carbs': 225,
        'fat': 55
    })
    
    # Create metrics layout
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        calories_progress = (daily_totals['calories'] / daily_goals['calories']) * 100
        st.metric(
            "Calories",
            f"{int(daily_totals['calories'])} / {daily_goals['calories']}",
            f"{calories_progress:.1f}%"
        )
        
    with col2:
        protein_progress = (daily_totals['protein'] / daily_goals['protein']) * 100
        st.metric(
            "Protein (g)",
            f"{int(daily_totals['protein'])} / {daily_goals['protein']}",
            f"{protein_progress:.1f}%"
        )
        
    with col3:
        carbs_progress = (daily_totals['carbs'] / daily_goals['carbs']) * 100
        st.metric(
            "Carbs (g)",
            f"{int(daily_totals['carbs'])} / {daily_goals['carbs']}",
            f"{carbs_progress:.1f}%"
        )
        
    with col4:
        fat_progress = (daily_totals['fat'] / daily_goals['fat']) * 100
        st.metric(
            "Fat (g)",
            f"{int(daily_totals['fat'])} / {daily_goals['fat']}",
            f"{fat_progress:.1f}%"
        )
    
    # Create macronutrient distribution chart
    fig = go.Figure(data=[
        go.Pie(
            labels=['Protein', 'Carbs', 'Fat'],
            values=[daily_totals['protein'] * 4, daily_totals['carbs'] * 4, daily_totals['fat'] * 9],
            hole=.3
        )
    ])
    
    fig.update_layout(
        title="Today's Macronutrient Distribution",
        height=400,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)
