import requests
import math

# Function to get elevation for multiple points
def get_elevations(coords):
    locations = '|'.join(f"{coord[0]},{coord[1]}" for coord in coords)
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={locations}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {f"{coord[0]},{coord[1]}": result['elevation'] for coord, result in zip(coords, data['results'])}
    else:
        print("Error fetching elevation data")
        return {}

# Function to calculate slope percentage
def calculate_slope(elevation_diff, distance):
    if distance == 0:
        return 0
    slope_percentage = (elevation_diff / distance) * 100
    return slope_percentage

# Main function to process multiple consecutive pairs of coordinates
# def process_elevation(graph):
#     # Get all nodes in the graph
#     nodes = list(graph.nodes(data=True))

#     # Create a dictionary to hold coordinates and elevations
#     coordinates = {node: (data['y'], data['x']) for node, data in nodes}

#     # Fetch elevations for all coordinates at once
#     elevation_data = get_elevations(coordinates.values())

#     # Loop through adjacent nodes in the graph
#     for node1, node2 in graph.edges():
#         lat1, lon1 = coordinates[node1]
#         lat2, lon2 = coordinates[node2]

#         # Retrieve elevation data from the results
#         elevation1 = elevation_data.get(f"{lat1},{lon1}")
#         elevation2 = elevation_data.get(f"{lat2},{lon2}")

#         if elevation1 is not None and elevation2 is not None:
#             # Calculate the elevation difference
#             elevation_diff = abs(elevation2 - elevation1)

#             # Calculate the distance between the two points
#             distance = calculate_distance(lat1, lon1, lat2, lon2)

#             # Calculate the slope in percentage
#             slope = calculate_slope(elevation_diff, distance)

#             # Print results based on slope percentage
#             print(f"Between Node {node1} and Node {node2}:")
#             print(f"  Elevation 1: {elevation1} meters")
#             print(f"  Elevation 2: {elevation2} meters")
#             print(f"  Distance: {distance:.2f} meters")
#             print(f"  Slope: {slope:.2f}%")
#             if slope > 10:
#                 print("  - Very Bad\n")
#             elif slope > 5:
#                 print("  - Bad\n")
#             else:
#                 print("  - Acceptable\n")