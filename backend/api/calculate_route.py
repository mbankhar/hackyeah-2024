import osmnx as ox
from flask import Flask, request, jsonify

app = Flask(__name__)

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
        Ax, Ay = data['start']
        Bx, By = data['end']
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid start or end coordinates"}), 400

    G = ox.load_graphml("./krakow3200m.graphml")    
    orig = ox.distance.nearest_nodes(G, Ay, Ax)
    dest = ox.distance.nearest_nodes(G, By, Bx)
    
    route = ox.shortest_path(G, orig, dest, weight="length")
    route = node_ids_to_coords(route, G)
    
    return jsonify(route)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
