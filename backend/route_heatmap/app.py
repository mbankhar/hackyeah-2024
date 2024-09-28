import osmnx as ox
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

def get_coordinates(address):
    # Hier müssen wir die CSV-Datei erstellen, die Adressen und Koordinaten enthält.
    csv_file = 'data/interpreter.csv'
    df = pd.read_csv(csv_file)

    # Wir nehmen an, dass die Adressen im Format "Straße Hausnummer" sind.
    street, house_number = address.rsplit(' ', 1)

    # Suche in der Tabelle nach der Adresse
    result = df[(df['addr:street'] == street) & (df['addr:housenumber'] == house_number)]

    if not result.empty:
        lat = result['@lat'].values[0]
        lon = result['@lon'].values[0]
        return (lat, lon)
    else:
        return None

@app.route('/calculate', methods=['POST'])
def calculate_route():
    try:
         data = request.get_json()
    except Exception as e:
        print(f"error: {e}")
    print("Received data:", data)  # Debugging-Ausdruck hinzufügen
    if not data:
        return jsonify({"error": "No data provided"}), 400

    if 'start' not in data or 'end' not in data:
        return jsonify({"error": "Start and end coordinates must be provided"}), 400

    try:
        A = data['start']
        B = data['end']
        print("Start address:", A)  # Debugging-Ausdruck hinzufügen
        print("End address:", B)     # Debugging-Ausdruck hinzufügen
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid start or end coordinates"}), 400

    Ax, Ay = get_coordinates(A)
    Bx, By = get_coordinates(B)
    G = ox.load_graphml("data/krakow3200m.graphml")
    orig = ox.distance.nearest_nodes(G, Ay, Ax)
    dest = ox.distance.nearest_nodes(G, By, Bx)
    route = ox.shortest_path(G, orig, dest, weight="length")
    return jsonify(route)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
