import osmnx as ox
from flask import Flask, request, jsonify
import pandas as pd

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
        # A = "Karmelicka 3"
        # B = "Doktora Ludwika Zamenhofa 10"
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid start or end coordinates"}), 400

    Ax, Ay = get_coordinates(A)
    Bx, By = get_coordinates(B)
    G = ox.load_graphml("../data/krakow3200m.graphml")    
    orig = ox.distance.nearest_nodes(G, Ay, Ax)
    dest = ox.distance.nearest_nodes(G, By, Bx)
    
    route = ox.shortest_path(G, orig, dest, weight="length")
    route = node_ids_to_coords(route, G)
    return jsonify(route)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
