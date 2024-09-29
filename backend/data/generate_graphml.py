import osmnx as ox
from astral import LocationInfo
from astral.sun import sun
from datetime import datetime
from elevation import calculate_slope
from elevation import get_elevations

def apply_rules(data, rules):
    length = data['length']
    for condition, adjustment in rules.items():
        if condition(data):
            length = length * adjustment
    return length

# Define the location to always be Kraków, Poland
city = LocationInfo("Kraków", "Poland")
def is_dark(city):
    """Check if it's currently dark based on sunrise and sunset times in Kraków."""
    s = sun(city.observer, date=datetime.now().date())
    current_time = datetime.now().time()
    return current_time > s['sunset'].time() or current_time < s['sunrise'].time()

def is_parking_relevant():
    """Check if the current time is between 6 AM and 10 PM."""
    current_time = datetime.now().time()
    return current_time >= datetime.strptime("06:00", "%H:%M").time() and current_time <= datetime.strptime("22:00", "%H:%M").time()

# Rules with Kraków location hardcoded and the requested conditions
rules = {
    # Lighting and time-based condition
    lambda data: is_dark(city) and data.get('lit') != 'yes': 2.0,  # Increase length if unlit and it is dark
    # Speed zones multipliers
    lambda data: data.get('maxspeed') and float(max(data['maxspeed'] if isinstance(data.get('maxspeed'), list) else [data.get('maxspeed')] or [0])) <= 30: 0.25,
    # lambda data: data.get('maxspeed') and float(data['maxspeed']) <= 30: 0.25,  # Reduce length if in a 30km/h speed zone
    lambda data: data.get('maxspeed') and 30 < float(max(data['maxspeed'] if isinstance(data.get('maxspeed'), list) else [data.get('maxspeed')] or [0])) <= 50: 0.5,
    # lambda data: data.get('maxspeed') and 30 < float(data['maxspeed']) <= 50: 0.5,  # Moderate length for 30-50 km/h speed zones
    lambda data: data.get('maxspeed') and float(max(data['maxspeed'] if isinstance(data.get('maxspeed'), list) else [data.get('maxspeed')] or [0])) > 50: 1.5,
    # lambda data: data.get('maxspeed') and float(data['maxspeed']) > 50: 1.5,  # Increase length for high-speed zones (over 50 km/h)
    # Road conditions
    lambda data: data.get('surface') in ['paved', 'asphalt']: 0.25,  # Safer surfaces
    lambda data: data.get('cycleway') is not None: 0.5,  # Prioritize cycle paths
    lambda data: data.get('smoothness') in ['excellent', 'good']: 0.5,  # Favor smooth paths
    # Traffic incidents and conditions
    lambda data: data.get('safety:traffic_incidents', 'unknown') != 'none': 2.0,  # Increase for past accidents
    lambda data: data.get('traffic:realtime', 'unknown') == 'high': 1.5,  # Increase for high real-time traffic
    lambda data: data.get('surface', 'unknown') == 'poor': 1.5,  # Increase for poor road quality
    # lambda data: data.get('traffic_lights_distance', 'unknown') > 500: 0.7,  # Decrease for safer distances between traffic lights
    lambda data: data.get('highway') == 'construction': 1.5,  # Increase for construction zones
    lambda data: data.get('width', 0) and float(min(data.get('width')) if isinstance(data.get('width'), list) else data.get('width')) > 5: 0.8,
    # Parking lanes, with time condition (irrelevant between 10 PM and 6 AM)
    lambda data: data.get('parking:lane', 'unknown') != 'no' and is_parking_relevant(): 1.2  # Increase if parking spots pose danger for bikes during relevant times
}

ox.settings.useful_tags_way += [
    "highway", 
    "cycleway", 
    "surface", 
    "smoothness", 
    "bike_lane", 
    "lanes", 
    "width", 
    "sidewalk", 
    "junction", 
    "bicycle", 
    "motor_vehicle", 
    "oneway", 
    "traffic_calming", 
    "condition", 
    "public_transport", 
    "landuse", 
    "hazard", 
    "access", 
    "vehicle"
]

place = (50.06215, 19.93632)
filepath = "./krakow3200m_marian.graphml"

G = ox.graph_from_point(place, dist=3200, network_type="bike")
def process_elevation(graph):
    # Get all nodes in the graph
    nodes = list(graph.nodes(data=True))

    # Create a dictionary to hold coordinates and elevations
    coordinates = {node: (data['y'], data['x']) for node, data in nodes}

    # Fetch elevations for all coordinates at once
    elevation_data = get_elevations(coordinates.values())

    # Loop through adjacent nodes in the graph
    for node1, node2, k, data in G.edges(data=True, keys=True):
        data['length'] = apply_rules(data, rules)
        lat1, lon1 = coordinates[node1]
        lat2, lon2 = coordinates[node2]

        # Retrieve elevation data from the results
        elevation1 = elevation_data.get(f"{lat1},{lon1}")
        elevation2 = elevation_data.get(f"{lat2},{lon2}")

        if elevation1 is not None and elevation2 is not None:
            # Calculate the elevation difference
            elevation_diff = abs(elevation2 - elevation1)

            # Calculate the distance between the two points
            distance = ox.distance.great_circle(lat1, lon1, lat2, lon2)
            slope = calculate_slope(elevation_diff, distance)
            if slope > 10:
                data['length'] = data['length'] * 5
            elif slope > 5:
                data['length'] = data['length'] * 3


ox.save_graphml(G, filepath)

#G = ox.load_graphml(filepath) use this to load the graph in subsequent work
