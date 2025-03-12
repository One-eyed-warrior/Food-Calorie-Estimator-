#!/bin/bash

# Create project directories
mkdir -p .streamlit assets components data utils

# Create .streamlit/config.toml
cat > .streamlit/config.toml << 'EOL'
[server]
headless = true
address = "0.0.0.0"
port = 5000

[theme]
primaryColor = "#4CAF50"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
EOL

# Create .env template
cat > .env << 'EOL'
SPOONACULAR_API_KEY=your_api_key_here
EOL

echo "Project structure created successfully!"
echo "Next steps:"
echo "1. Install Python requirements: pip install streamlit pillow plotly requests numpy tflite-runtime"
echo "2. Add your Spoonacular API key to .env file"
echo "3. Run the app: streamlit run app.py"
