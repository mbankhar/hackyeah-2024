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

place = (50.067730, 19.991220)
G = ox.graph_from_point(place, dist=1600, network_type="bike")
ox.save_graphml(G, "tauron1600m.graphml")
