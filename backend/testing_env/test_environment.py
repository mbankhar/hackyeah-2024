import osmnx as ox

G = ox.load_graphml("../data/krakow3200m.graphml")
Ax, Ay = (50.06222, 19.93182)
Bx, By = (50.06470, 19.94703)
orig = ox.distance.nearest_nodes(G, Ay, Ax)
dest = ox.distance.nearest_nodes(G, By, Bx)

route = ox.shortest_path(G, orig, dest, weight="length")
route_edges = ox.routing.route_to_gdf(G, route, weight="length")
m = route_edges.explore(tiles="cartodbpositron", style_kwds={"weight": 5})

print("Im working")
m.save("./map.html")