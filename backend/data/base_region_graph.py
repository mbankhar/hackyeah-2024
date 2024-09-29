import osmnx as ox

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

place = (50.06268, 19.93752)
G = ox.graph_from_point(place, dist=3200, network_type="bike")
ox.save_graphml(G, "krakow3200v2.graphml")
