import streamlit as st
from PIL import Image
import numpy as np
from utils.food_recognition import FoodRecognizer

def render_camera_scanner():
    st.header("📸 Scan Food with Camera")

    # Initialize food recognizer
    food_recognizer = FoodRecognizer()

    # Camera input using Streamlit's native component
    camera_image = st.camera_input("Take a picture of your food")

    if camera_image is not None:
        # Display the captured image
        image = Image.open(camera_image)
        st.image(image, caption="Captured Food Image", use_container_width=True)

        with st.spinner('Analyzing food image...'):
            # Recognize food from image
            recognition_result = food_recognizer.recognize_food(image)

            if recognition_result['success']:
                st.success("Food recognized successfully!")

                # Display recognition results
                st.subheader("Recognition Results")
                st.write(f"Category: {recognition_result['category']}")
                st.write(f"Confidence: {recognition_result['probability']*100:.1f}%")

                # Get nutritional information
                nutrition = recognition_result['nutrition']

                # Display nutritional information
                st.subheader("Nutritional Information (per 100g)")
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Calories", f"{nutrition['calories']} kcal")
                with col2:
                    st.metric("Protein", f"{nutrition['protein']}g")
                with col3:
                    st.metric("Carbs", f"{nutrition['carbs']}g")
                with col4:
                    st.metric("Fat", f"{nutrition['fat']}g")

                # Manual confirmation and portion adjustment
                st.subheader("Confirm and Log")

                # Allow manual override of food name
                food_name = st.text_input("Food Name", value=recognition_result['category'])

                # Portion size
                portion_size = st.number_input(
                    "Portion Size (servings)",
                    min_value=0.25,
                    max_value=10.0,
                    value=1.0,
                    step=0.25
                )

                # Add to food log button
                if st.button("Add to Food Log"):
                    if food_name:
                        # Here we would typically integrate with the food database
                        st.success(f"Added {portion_size} portion(s) of {food_name} to your food log!")
                    else:
                        st.warning("Please enter a food name")
            else:
                st.error(f"Failed to recognize food: {recognition_result.get('error', 'Unknown error')}")

                # Fallback to manual entry
                st.subheader("Manual Food Entry")
                food_categories = [
                    "Fruits and Vegetables",
                    "Grains and Breads",
                    "Protein Foods",
                    "Dairy Products",
                    "Snacks and Desserts"
                ]

                selected_category = st.selectbox(
                    "Select Food Category",
                    food_categories
                )

                food_name = st.text_input("Food Name")
                portion_size = st.number_input(
                    "Portion Size",
                    min_value=0.25,
                    max_value=10.0,
                    value=1.0,
                    step=0.25
                )

                if st.button("Add to Food Log"):
                    if food_name:
                        st.success(f"Added {portion_size} portion(s) of {food_name} to your food log!")
                    else:
                        st.warning("Please enter a food name")
    else:
        st.info("Click the button above to activate your camera and take a picture of your food.")

    # Add tips for better food photos
    with st.expander("📸 Tips for Better Food Photos"):
        st.markdown("""
        - Ensure good lighting
        - Center the food in the frame
        - Take the photo from above
        - Include the entire plate/bowl
        - Avoid blurry photos
        """)