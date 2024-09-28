import osmnx as ox

G = ox.load_graphml("./krakow1000m.graphml")

ec = ox.plot.get_edge_colors_by_attr(G, attr="length", cmap="inferno_r")
fig, ax = ox.plot_graph(
    G, node_size=0, show=False, edge_color=ec, edge_linewidth=3, save=True, filepath="./map2.jpg"
)