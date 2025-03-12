import requests
import os
import base64
from io import BytesIO
from PIL import Image

class FoodRecognizer:
    def __init__(self):
        self.api_key = os.environ.get('SPOONACULAR_API_KEY')
        self.base_url = "https://api.spoonacular.com/food/images/classify"

    def recognize_food(self, image):
        """
        Analyze food image using Spoonacular API
        """
        try:
            # Convert image to file-like object
            img_byte_arr = BytesIO()
            image.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()

            # Prepare API request
            files = {
                'file': ('image.jpg', img_byte_arr, 'image/jpeg')
            }

            params = {
                'apiKey': self.api_key
            }

            # Make API request
            response = requests.post(
                self.base_url,
                files=files,
                params=params
            )

            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'category': result.get('category', ''),
                    'probability': result.get('probability', 0),
                    'nutrition': self.get_food_info(result.get('category', ''))
                }
            else:
                return {
                    'success': False,
                    'error': f"API Error: {response.status_code} - {response.text}"
                }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def get_food_info(self, category):
        """
        Get nutritional information for recognized food category
        """
        try:
            # Search for food items matching the category
            search_url = "https://api.spoonacular.com/food/ingredients/search"
            params = {
                'query': category,
                'number': 1,
                'apiKey': self.api_key
            }

            response = requests.get(search_url, params=params)

            if response.status_code == 200 and response.json().get('results'):
                # Get detailed nutrition info
                ingredient_id = response.json()['results'][0]['id']
                info_url = f"https://api.spoonacular.com/food/ingredients/{ingredient_id}/information"
                params = {
                    'amount': 100,
                    'unit': 'g',
                    'apiKey': self.api_key
                }

                info_response = requests.get(info_url, params=params)

                if info_response.status_code == 200:
                    nutrition = info_response.json().get('nutrition', {})
                    return {
                        'calories': nutrition.get('calories', 0),
                        'protein': nutrition.get('protein', 0),
                        'carbs': nutrition.get('carbs', 0),
                        'fat': nutrition.get('fat', 0)
                    }

            return {
                'calories': 0,
                'protein': 0,
                'carbs': 0,
                'fat': 0
            }

        except Exception as e:
            return {
                'calories': 0,
                'protein': 0,
                'carbs': 0,
                'fat': 0
            }