import osmnx as ox
from flask import Flask, request, jsonify
import pandas as pd
import folium
from folium.plugins import HeatMap

app = Flask(__name__)

def get_coordinates(address):
    csv_file = '../data/interpreter.csv'
    # Read the CSV file
    df = pd.read_csv(csv_file, delimiter='\t')

    # Split the address into street and house number
    street, house_number = address.rsplit(' ', 1)

    # Filter the DataFrame for the matching street and house number
    result = df[(df['addr:street'] == street) & (df['addr:housenumber'] == house_number)]

    # If a match is found, return the coordinates
    if not result.empty:
        lat = result['@lat'].values[0]
        lon = result['@lon'].values[0]
        return (lat, lon)
    else:
        return None  # or raise an exception

def node_ids_to_coords(route, G):
    coords = []
    for node_id in route:
        lat = G.nodes[node_id]['y']
        lon = G.nodes[node_id]['x']
        coords.append((lat, lon))
    return coords

def update_usage_counts(route, G):
    for u, v in route:
        G.edges[u, v, 0]['usage_count'] += 1

def create_heatmap(G):
    # Prepare data for heatmap
    heat_data = []
    for u, v, data in G.edges(data=True):
        # Append the (latitude, longitude, intensity) for each edge
        if 'usage_count' in data:
            lat1 = G.nodes[u]['y']
            lon1 = G.nodes[u]['x']
            lat2 = G.nodes[v]['y']
            lon2 = G.nodes[v]['x']
            # Average the coordinates to represent the edge
            avg_lat = (lat1 + lat2) / 2
            avg_lon = (lon1 + lon2) / 2
            # Add heatmap point: (lat, lon, intensity)
            heat_data.append((avg_lat, avg_lon, data['usage_count']))

    # Create a map centered around Kraków
    m = folium.Map(location=[50.06215, 19.93632], zoom_start=13)
    HeatMap(heat_data).add_to(m)

    # Save the heatmap
    m.save("heatmap.html")

@app.route('/calculate', methods=['POST'])
def calculate_route():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    if 'start' not in data or 'end' not in data:
        return jsonify({"error": "Start and end coordinates must be provided"}), 400

    try:
        A = data['start']
        B = data['end']
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid start or end coordinates"}), 400

    Ax, Ay = get_coordinates(A)
    Bx, By = get_coordinates(B)
    G = ox.load_graphml("../data/krakow3200m.graphml")

    # Initialize usage count for edges if not already done
    for u, v, k, data in G.edges(data=True, keys=True):
        if 'usage_count' not in data:
            data['usage_count'] = 0

    orig = ox.distance.nearest_nodes(G, Ay, Ax)
    dest = ox.distance.nearest_nodes(G, By, Bx)
    route = ox.shortest_path(G, orig, dest, weight="length")
    route_coords = node_ids_to_coords(route, G)

    # Update usage counts for the edges in the route
    update_usage_counts(route, G)

    # Create heatmap
    create_heatmap(G)

    return jsonify(route_coords)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
