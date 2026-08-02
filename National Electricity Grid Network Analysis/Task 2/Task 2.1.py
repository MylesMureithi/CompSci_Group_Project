import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

utilities = pd.read_csv('utilities.csv') # utilities.csv
substations = pd.read_csv('substations.csv') # substations.csv
lines = pd.read_csv('lines.csv') # lines.csv


# Create network graph — undirected, since AC power can flow either way
# along a line depending on system conditions (unlike a scheduled flight,
# which always has a fixed origin and destination)

# Add substations as nodes with attributes (region, voltage, coordinates, etc.)
# Add lines as edges with weights (length, capacity, etc.)

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Create an undirected graph
G = nx.Graph()

# -------------------------------------------------
# 1. Add substations as nodes
# -------------------------------------------------

for index, substation in substations.iterrows():

    substation_id = substation["Substation ID"]

    G.add_node(
        substation_id,
        name=substation["Name"],
        region=substation["Region"],
        status=substation["Status"]
    )


# -------------------------------------------------
# 2. Add transmission lines as edges
# -------------------------------------------------

for index, line in lines.iterrows():

    source_substation = line["Source Substation ID"]
    destination_substation = line["Destination Substation ID"]

    # Add the line only when both substations exist
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


# -------------------------------------------------
# 3. Display basic graph information
# -------------------------------------------------

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
# - Node centrality measures (degree, betweenness, closeness, PageRank)
# - Network diameter and average path length
# - Clustering coefficients
# - Community detection
# - Critical-substation identification
 
# Analyse network structure
# - Identify the most-connected substations (regional 'superhubs')
# - Find bridge lines (critical single points of connection)
# - Detect isolated components
# - Measure network efficiency


