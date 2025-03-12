import streamlit as st

def render_food_logger(data_manager):
    st.header("Log Your Food")
    
    with st.form("food_logger"):
        food_items = data_manager.get_food_items()
        selected_food = st.selectbox("Select Food", food_items)
        
        portions = st.number_input(
            "Portions",
            min_value=0.25,
            max_value=10.0,
            value=1.0,
            step=0.25
        )
        
        food_info = data_manager.get_food_info(selected_food)
        
        # Preview nutritional info
        st.write("Nutritional Information (per portion):")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.write(f"Calories: {food_info['calories']}")
        with col2:
            st.write(f"Protein: {food_info['protein']}g")
        with col3:
            st.write(f"Carbs: {food_info['carbs']}g")
        with col4:
            st.write(f"Fat: {food_info['fat']}g")
            
        submitted = st.form_submit_button("Log Food")
        
        if submitted:
            data_manager.log_meal(selected_food, portions)
            st.success(f"Logged {portions} portion(s) of {selected_food}")
