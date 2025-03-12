import streamlit as st
from utils.data_manager import DataManager
from utils.nutrition_calculator import NutritionCalculator
from components.dashboard import render_dashboard
from components.food_logger import render_food_logger
from components.progress_charts import render_progress_charts
from components.camera_scanner import render_camera_scanner

# Page configuration
st.set_page_config(
    page_title="Nutrition Tracker",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed"  # Start with collapsed sidebar on mobile
)

# Load custom CSS
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Add viewport meta tag for mobile responsiveness
st.markdown(
    """
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" />
    """,
    unsafe_allow_html=True
)

# Initialize data manager
data_manager = DataManager()

# Sidebar for user settings
with st.sidebar:
    st.title("⚙️ Settings")

    # User profile
    st.subheader("Profile Settings")

    # Make inputs more mobile-friendly
    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input(
            "Weight (kg)",
            min_value=30,
            max_value=200,
            value=70,
            step=1
        )
    with col2:
        height = st.number_input(
            "Height (cm)",
            min_value=100,
            max_value=250,
            value=170,
            step=1
        )

    age = st.number_input("Age", min_value=15, max_value=100, value=30)
    gender = st.selectbox("Gender", ["Male", "Female"])
    activity_level = st.selectbox(
        "Activity Level",
        ["Sedentary", "Light", "Moderate", "Active", "Very Active"]
    )

    # Calculate daily needs
    if st.button("Calculate Daily Needs", use_container_width=True):
        daily_needs = NutritionCalculator.calculate_daily_needs(
            weight, height, age, gender, activity_level
        )
        st.session_state.daily_goals = daily_needs
        st.success("Daily goals updated!")

# Main content
st.title("🥗 Nutrition Tracker")

# Make image responsive
st.markdown(
    """
    <style>
    img {
        max-width: 100%;
        height: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.image(
    "https://images.unsplash.com/photo-1498579809087-ef1e558fd1da",
    caption="Eat healthy, live better!",
    use_container_width=True
)

# Main content tabs - made more touch-friendly
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Dashboard",
    "📝 Log Food",
    "📸 Scan Food",
    "📈 Progress"
])

with tab1:
    render_dashboard(data_manager)

with tab2:
    render_food_logger(data_manager)

with tab3:
    render_camera_scanner()

with tab4:
    render_progress_charts(data_manager)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 1rem;'>
        <p style='margin: 0;'>Made with ❤️ for a healthier you!</p>
    </div>
    """,
    unsafe_allow_html=True
)