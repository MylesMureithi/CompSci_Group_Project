import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import statistics as stat

utilities = pd.read_csv('utilities.csv') # utilities.csv
substations = pd.read_csv('substations.csv') # substations.csv
lines = pd.read_csv('lines.csv') # lines.csv


# Create network graph — undirected, since AC power can flow either way
# along a line depending on system conditions (unlike a scheduled flight,
# which always has a fixed origin and destination)

# Add substations as nodes with attributes (region, voltage, coordinates, etc.)
# Add lines as edges with weights (length, capacity, etc.)


# Create an undirected graph
G = nx.Graph()

for index, substation in substations.iterrows():

    substation_id = substation["Substation ID"]

    G.add_node(
        substation_id,
        name=substation["Name"],
        region=substation["Region"],
        status=substation["Status"]
    )

for index, line in lines.iterrows():

    source_substation = line["Source Substation ID"]
    destination_substation = line["Destination Substation ID"]


    if (
        source_substation in G.nodes
        and destination_substation in G.nodes
    ):

        G.add_edge(
            source_substation,
            destination_substation,
            line_type=line["Line Type"],
            status=line["Status"]
        )

    else:
        print(
            "Orphaned line:",
            source_substation,
            "to",
            destination_substation
        )


print("Number of substations:", G.number_of_nodes())
print("Number of transmission lines:", G.number_of_edges())

print("\nSubstations:")
print(G.nodes(data=True))

print("\nTransmission lines:")
print(G.edges(data=True))


# -------------------------------------------------
# 4. Draw the electricity network
# -------------------------------------------------

plt.figure(figsize=(14, 10))

network_positions = nx.spring_layout(G, seed=42)

nx.draw(
    G,
    network_positions,
    with_labels=True,
    node_size=700,
    font_size=7
)

plt.title("National Electricity Grid Network")
plt.show()


# Calculate network metrics
data = [
    ['Length (km)']
]

# - Node centrality measures (degree, betweenness, closeness, PageRank)
node_degree = list(G.degree())
node_betweenness = nx.betweenness_centrality(G)
node_closeness = nx.closeness_centrality(G)
node_pagerank = nx.pagerank(G)

print(node_degree)
print(node_betweenness)
print(node_closeness)

for key, value in node_pagerank.items():
    print(f"Node {key}: {value:.3f}")

# - Network diameter and average path length
connected = nx.connected_components(G)
max_connect = max(connected, key=len)

sub = G.subgraph(max_connect)
diameter = nx.diameter(sub)
print(diameter)

print(stat.mean(lines[data[0][0]]))

# - Clustering coefficients
clustered = nx.clustering(G)

for key, value in clustered.items():
    print(f"Node {key}: {value:.1f}")

comm = nx.community.louvain_communities(G)
print(comm)

# community detection
"""communities = {}

countries = substations['Country'].unique()

for country in countries:
    # Get unique regions specific to this country
    regions_in_country = substations[substations['Country'] == country]['Region'].unique()
    
    communities[country] = {}
    
    for reg in regions_in_country:
        # Grouping logic: filter stations matching both country and region, then extract their names/short names
        filtered_stations = substations[
            (substations['Country'] == country) & 
            (substations['Region'] == reg)
        ]['Name'].tolist() # or use the 'Name' column depending on what you need
        
        communities[country][reg] = filtered_stations

print(communities)
"""

# - Critical-substation identification

 




# Analyse network structure
# - Identify the most-connected substations (regional 'superhubs')
# - Find bridge lines (critical single points of connection)
# - Detect isolated components
# - Measure network efficiency


