from flask import Flask, render_template, jsonify, request
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Aladhan API endpoint for prayer times
API_URL = "http://api.aladhan.com/v1/timings"

# Get OpenCage API key from environment variable
OPENCAGE_API_KEY = os.getenv('OPENCAGE_API_KEY')

# Check if the API key is loaded correctly
if not OPENCAGE_API_KEY:
    raise ValueError("API key for OpenCage is missing. Please set it in the .env file.")

# Function to get latitude and longitude for a given city name
def get_lat_lng(city_name):
    geocode_url = f"https://api.opencagedata.com/geocode/v1/json?q={city_name}&key={OPENCAGE_API_KEY}"
    response = requests.get(geocode_url)
    
    # Check if the API request was successful (status code 200)
    if response.status_code != 200:
        return None, None

    data = response.json()

    # Log the response for debugging
    print(f"OpenCage API Response: {data}")

    if data['results']:
        lat = data['results'][0]['geometry']['lat']
        lng = data['results'][0]['geometry']['lng']
        return lat, lng
    else:
        return None, None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_prayer_times', methods=['GET'])
def get_prayer_times():
    # Get the city name from the request
    city_name = request.args.get('city', '')
    
    if not city_name:
        return jsonify({'error': 'City name is required'}), 400

    # Get latitude and longitude for the given city
    latitude, longitude = get_lat_lng(city_name)
    
    if latitude is None or longitude is None:
        return jsonify({'error': 'Invalid city name or unable to fetch coordinates'}), 400

    # Get current date
    today = datetime.today().strftime('%Y-%m-%d')

    # Log the URL for Aladhan API request
    print(f"Requesting prayer times from Aladhan API: {API_URL}?latitude={latitude}&longitude={longitude}&method=2&date={today}")

    # Make a request to the Aladhan API
    response = requests.get(f"{API_URL}?latitude={latitude}&longitude={longitude}&method=2&date={today}")
    data = response.json()

    # Debugging: print Aladhan response
    print(f"Aladhan API Response: {data}")

    if data['code'] == 200:
        timings = data['data']['timings']
        return jsonify(timings)
    else:
        return jsonify({'error': 'Could not fetch prayer times'}), 400

if __name__ == "__main__":
    app.run(debug=True)
