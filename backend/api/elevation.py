import requests
import json
import math
import concurrent.futures

# Function to get elevation for multiple points
def get_elevations(coords):
    locations = '|'.join(f"{coord['latitude']},{coord['longitude']}" for coord in coords)
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={locations}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {f"{coord['latitude']},{coord['longitude']}": result['elevation'] for coord, result in zip(coords, data['results'])}
    else:
        print("Error fetching elevation data")
        return {}

# Function to calculate distance between two points using Haversine formula
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c  # Distance in kilometers
    return distance * 1000  # Convert to meters

# Function to calculate slope percentage
def calculate_slope(elevation_diff, distance):
    if distance == 0:
        return 0
    slope_percentage = (elevation_diff / distance) * 100
    return slope_percentage

# Main function to process multiple consecutive pairs of coordinates
def process_coordinates(filename='elevation.json'):
    # Load coordinates from JSON file
    with open(filename, 'r') as f:
        data = json.load(f)

    # Fetch elevations for all coordinates at once
    elevation_data = get_elevations(data)

    # Loop through consecutive pairs of coordinates
    for i in range(len(data) - 1):
        lat1, lon1 = data[i]['latitude'], data[i]['longitude']
        lat2, lon2 = data[i + 1]['latitude'], data[i + 1]['longitude']

        # Retrieve elevation data from the results
        elevation1 = elevation_data.get(f"{lat1},{lon1}")
        elevation2 = elevation_data.get(f"{lat2},{lon2}")

        if elevation1 is not None and elevation2 is not None:
            # Calculate the elevation difference
            elevation_diff = abs(elevation2 - elevation1)

            # Calculate the distance between the two points
            distance = calculate_distance(lat1, lon1, lat2, lon2)

            # Calculate the slope in percentage
            slope = calculate_slope(elevation_diff, distance)

            # Print results based on slope percentage
            if slope > 10:
                print(f"Between Point {i+1} and Point {i+2}:")
                print(f"  Elevation 1: {elevation1} meters")
                print(f"  Elevation 2: {elevation2} meters")
                print(f"  Distance: {distance:.2f} meters")
                print(f"  Slope: {slope:.2f}% - Very Bad\n")
            elif slope > 5:
                print(f"Between Point {i+1} and Point {i+2}:")
                print(f"  Elevation 1: {elevation1} meters")
                print(f"  Elevation 2: {elevation2} meters")
                print(f"  Distance: {distance:.2f} meters")
                print(f"  Slope: {slope:.2f}% - Bad\n")

# Example usage
process_coordinates()
