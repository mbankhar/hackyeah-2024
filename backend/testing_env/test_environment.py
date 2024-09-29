import osmnx as ox
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# Load the graphs
G1 = ox.load_graphml("../data/tauron_safe_rate_1.graphml")
G2 = ox.load_graphml("../data/tauron_safe_rate_2.graphml")
G3 = ox.load_graphml("../data/tauron_safe_rate_3.graphml")
G4 = ox.load_graphml("../data/tauron_safe_rate_4.graphml")
G5 = ox.load_graphml("../data/tauron_safe_rate_5.graphml")

# Get a list of nodes
nodes = list(G1.nodes())
A = nodes[0]
B = nodes[-1]

# Calculate shortest paths
routes = [
    ox.shortest_path(G, A, B, weight="length") for G in [G1, G2, G3, G4, G5]
]

# Get edges GeoDataFrame
nodes_gdf, edges_gdf = ox.graph_to_gdfs(G1)

# Define colors for each route
colors = ["#FF0000", "#FFA500", "#FFFF00", "#ADFF2F", "#00FF00"]

# Create a base figure
fig, ax = plt.subplots(figsize=(10, 10))

# Plot the base map
edges_gdf.plot(ax=ax, color="#222222", linewidth=1)

# Plot each route with its corresponding color
for route, color in zip(routes, colors):
    route_edges_gdf = ox.routing.route_to_gdf(G1, route, weight="length")
    route_edges_gdf.plot(ax=ax, color=color, linewidth=5, alpha=0.7)

# Create a legend
legend_labels = ["Fastest Route (G1)", "Fast but Less Safe (G2)", 
                 "Moderate Speed & Safety (G3)", "Safer but Slower (G4)", "Safest Route (G5)"]
legend_patches = [Patch(color=color, label=label) for color, label in zip(colors, legend_labels)]

# Add the legend to the figure
ax.legend(handles=legend_patches, loc='upper left', bbox_to_anchor=(1, 1), title="Routes")

# Save the figure as an image
plt.axis('off')  # Hide the axis
plt.savefig("./map_with_legend.png", bbox_inches='tight', dpi=300)
plt.close()  # Close the plot
