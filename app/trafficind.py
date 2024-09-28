import json
import os
import requests
from dotenv import load_dotenv  # Import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variable
api_key = os.getenv("TOMTOM_API_KEY")

# Check if the API key is loaded
if api_key is None:
    print("API key not found. Please set the TOMTOM_API_KEY in the .env file.")
    exit(1)

def load_coordinates(filename='coordinates.json'):
    with open(filename) as f:
        data = json.load(f)
    return data  # Simply return the list

# Function to get max speed data from OpenStreetMap using Overpass API
def get_max_speed_data(lat, lon):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    (way(around:50,{lat},{lon})["maxspeed"];);
    out body;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    if response.status_code == 200:
        data = response.json()
        speeds = []
        for element in data.get('elements', []):
            if 'tags' in element and 'maxspeed' in element['tags']:
                try:
                    speeds.append(int(element['tags']['maxspeed'].replace(' km/h', '').replace(' mph', '')))
                except ValueError:
                    continue
        return speeds
    else:
        return []

# Function to get traffic data for a single point
def get_traffic_data(lat, lon):
    url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={lat},{lon}&key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        current_speed = data.get('flowSegmentData', {}).get('currentSpeed', 0)
        return current_speed
    else:
        return None

# Main function to calculate average traffic level
def calculate_average_traffic_level():
    coordinates = load_coordinates()  # Load coordinates from JSON file
    traffic_levels = []

    for point in coordinates:
        latitude, longitude = point  # Unpacking latitude and longitude

        # Get max speed data for the current point
        max_speeds = get_max_speed_data(latitude, longitude)
        
        if max_speeds:
            max_speed = round(sum(max_speeds) / len(max_speeds))

            # Get current speed from TomTom
            current_speed = get_traffic_data(latitude, longitude)
            
            if current_speed is not None:
                effective_speed = min(current_speed, max_speed)
                if max_speed > 0:
                    traffic_level = (effective_speed / max_speed) * 100
                    traffic_levels.append(traffic_level)

    if traffic_levels:
        average_traffic_level = sum(traffic_levels) / len(traffic_levels)
    else:
        average_traffic_level = 0  # No valid traffic levels available

    # Print the final average traffic level
    print(f"Final Average Traffic Level: {average_traffic_level:.2f}%")

if __name__ == '__main__':
    calculate_average_traffic_level()
