import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import statistics as stat

utilities = pd.read_csv('grid-analysis/data_files/utilities.csv') # utilities.csv
substations = pd.read_csv('grid-analysis/data_files/substations.csv') # substations.csv
lines = pd.read_csv('grid-analysis/data_files/lines.csv') # lines.csv


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

print()
print("|", "="*65, "|")
print("\t\t\tGeneral Statistics: ")
print("→ Number of substations:", G.number_of_nodes())
print("→ Number of transmission lines:", G.number_of_edges())

print("\nSubstations:")
print(G.nodes(data=True))

print("\nTransmission lines:")
print(G.edges(data=True))

print()
# Draw the electricity network

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


# Calculate network metrics
data = [
    ['Length (km)']
]

# - Node centrality measures (degree, betweenness, closeness, PageRank)
node_degree = list(G.degree())
node_betweenness = nx.betweenness_centrality(G)
node_closeness = nx.closeness_centrality(G)
node_pagerank = nx.pagerank(G)

print()
print("|", "="*70, "|")
print("\t\t\tNode Centrality Measures")
print("→ Node Degree:")
print(node_degree)
print()

print("→ Node Betweenness:")
for key, value in node_betweenness.items():
    print(f"Node {key}: {value:.3f}")
print()

print("→ Node Closeness:")
for key, value in node_closeness.items():
    print(f"Node {key}: {value:.3f}")
print()

print("→ Node PageRank:")
for key, value in node_pagerank.items():
    print(f"Node {key}: {value:.3f}")
print()

# - Network diameter and average path length
connected = nx.connected_components(G)
max_connect = max(connected, key=len)

sub = G.subgraph(max_connect)
diameter = nx.diameter(sub)
print(f"Network Diameter: {diameter}")

print()
print(f"Average Path Length: {stat.mean(lines[data[0][0]]):.3f}")
print()

# - Clustering coefficients
clustered = nx.clustering(G)

print("Clustering Coefficients:")
for key, value in clustered.items():
    print(f"Node {key}: {value:.2f}")
print()

comm = nx.community.louvain_communities(G)

print("Community Detection: ")
print(comm)
print()


# community detection
communities = {}

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

print("Filtered Stations by Country and Region: ")
for key, value in communities.items():
    print(f"{key}: {value}\n")

print()

# - Critical-substation identification
rank_median = stat.median(node_pagerank.values())

substation_name = list(substations["Name"])
regions = list(substations["Region"])

print("Most connected substations by importance (%):")
for key, value in node_pagerank.items():
    if value > rank_median:
        print(f"'{substation_name[key - 1]}', Region '{regions[key - 1]}': {value*100:.1f}%")

print()

# Analyse network structure
# - Find bridge lines (critical single points of connection)            
edge_centrality = nx.edge_betweenness_centrality(G)
sorted_edges = sorted(edge_centrality.items(), key=lambda x: x[1], reverse=True)

print("Critical bridge lines:")
for edge, score in sorted_edges[:10]:  # top 10
    print(f"{edge}: {score:.4f}")

print()

# - Detect isolated components
source_substation = list(lines["Source Substation ID"])
destination_substation = list(lines["Destination Substation ID"])
substation_ids = list(substations["Substation ID"])

for value in substation_ids:
    if value not in source_substation and value not in  destination_substation:
        print(f"Substation '{substation_name[value - 1]}' is isolated.")

print()

# - Measure network efficiency
print(f"The network efficiency is at {nx.global_efficiency(G):.3f}%, meaning that it operates at approx. {(nx.global_efficiency(G))*100:.1f}% of its possible efficiency.")
print()

# Plotting the network
plt.show()

