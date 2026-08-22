import pandas as pd
import statistics as stat
from datetime import datetime
import networkx as nx
import matplotlib.pyplot as plt

utilities = pd.read_csv('National Electricity Grid Network Analysis/data_files/utilities.csv') # utilities.csv
substations = pd.read_csv('National Electricity Grid Network Analysis/data_files/substations.csv') # substations.csv
lines = pd.read_csv('National Electricity Grid Network Analysis/data_files/lines.csv') # lines.csv


# Load and capacity analysis
# - Utility footprint by number of substations and lines, per region
utility_ali = list(utilities['Alias'])
line_utility_ids = list(lines['Utility ID'])

line_util_alias = {}

for id in line_utility_ids:
    alias = utility_ali[id - 1]
    
    if alias in line_util_alias:
        line_util_alias[alias] += 1
    else:
        line_util_alias[alias] = 1

print()

utility_ali = list(utilities['Alias'])
util_country = list(utilities['Country'])
subs_country = list(substations['Country'])

# Create a mapping from Country to Utility Alias
country_to_alias = {}
for i, country in enumerate(util_country):
    country_to_alias[country] = utility_ali[i]

subs_util_alias = {}

for country in subs_country:
    alias = country_to_alias.get(country, "Unknown")

    if alias in subs_util_alias:
        subs_util_alias[alias] += 1
    else:
        subs_util_alias[alias] = 1

# print(subs_util_alias) → reveals 6 "Unknown" substations due to mismatching 'Country' names in Utilities.

print("|", "="*45, "|")
print("Utility Classification by Substations and Lines: ")
for util, line, subs in zip(line_util_alias.keys(), line_util_alias.values(), subs_util_alias.values()):
    print(f"Utility {util} has {subs} substations and {line} lines.")

print()

# - Identify substations operating close to rated capacity (upgrade candidates)
voltage = list(substations['Voltage (kV)'])
capacity = list(substations['Capacity (MVA)'])
sub_names = list(substations['Name'])

print("|", "="*45, "|")
print("Capacity Classifications: ")

volt_cap_ratio = {}

for name, volt, cap in zip(sub_names, voltage, capacity):
    # We prevent division by zero just in case
    if volt > 0:
        capacity_ratio = cap / volt
    else:
        capacity_ratio = 0.0
        
    volt_cap_ratio[name] = round(capacity_ratio, 3)


cap_mean = stat.mean(volt_cap_ratio.values())
cap_sdev = stat.stdev(volt_cap_ratio.values())

for key, value in zip(volt_cap_ratio.keys(), volt_cap_ratio.values()):
    if value > (cap_mean + cap_sdev):
        print(f"{key} is close to max capacity!")
    else:
        print(f"{key} is less than max capacity.")

print()

# - Analyse utility asset age using Commissioning Year
current_year = datetime.today().year
comm_years = list(substations['Commissioning Year'])
# sub_names = list(substations['Name'])

print("|", "="*60, "|")
print("Substation Classification by Age: ")
def year_calc():
    new_stations = dict(sorted({}))
    midlife_stations = dict(sorted({}))
    aged_stations = dict(sorted({}))

    for name, year in zip(sub_names, comm_years):
        diff = current_year - year
        if diff <= 15:
            new_stations[name] = f"{diff} years old"
        elif 16 <= diff <= 25:
            midlife_stations[name] = f"{diff} years old"
        else:
            aged_stations[name] = f"{diff} years old"

    ordered_new_stations = dict(sorted(new_stations.items()))
    ordered_midlife_stations = dict(sorted(midlife_stations.items()))
    ordered_aged_stations = dict(sorted(aged_stations.items()))

    return f"\nYounger Stations (< 15 yrs):\n{ordered_new_stations}\n\nMid-life Stations (16 - 25yrs):\n{ordered_midlife_stations}\n\nAged Stations (> 25 yrs):\n{ordered_aged_stations}\n\n"

print(year_calc())

# Reliability metrics
# - Proportion of lines 'Under Maintenance' by region/utility
substation_region = dict(zip(substations["Substation ID"], substations["Region"]))
utility_name = dict(zip(utilities["Utility ID"], utilities["Name"]))

totals = {}
maintenance = {}

for i, line in lines.iterrows():

    region = substation_region[line["Source Substation ID"]]
    utility = utility_name[line["Utility ID"]]

    key = (region, utility)

    totals[key] = totals.get(key, 0) + 1

    if line["Status"] == "Under Maintenance":
        maintenance[key] = maintenance.get(key, 0) + 1


print("Proportion of lines 'Under Maintenance' by region/utility:")
print("-"*100)

for key in totals:
    region, utility = key
    total_lines = totals[key]
    maintenance_lines = maintenance.get(key, 0)
    proportion = maintenance_lines/total_lines

    print(f"{region} region, Utility: {utility} is {proportion*100}% under maintenance.")

print()


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

node_betweenness = nx.betweenness_centrality(G)

line_ids = list(lines['Line ID'])

LENGTH_COL = 'Length (km)'
 
def minmax_100(values):
    """Rescale values to 0-100 (min -> 0, max -> 100). Falls back to zeros if no variance."""
    min_v = min(values)
    max_v = max(values)
 
    if max_v == min_v:
        return [0.0 for _ in values]
 
    return [100 * (v - min_v) / (max_v - min_v) for v in values]


reliability_rows = []

for _, line in lines.iterrows():

    line_id = line['Line ID']
    source = line['Source Substation ID']
    destination = line['Destination Substation ID']
    status = line['Status']

    # Skip lines whose endpoints aren't in the graph (should mirror the "Orphaned line" check above)
    if source not in G.nodes or destination not in G.nodes:
        continue

    # 1) Maintenance factor: 1 if under maintenance, else 0
    maintenance_factor = 1 if status == "Under Maintenance" else 0

    # 2) Raw line length (NaN-safe)
    length_km = line[LENGTH_COL] if LENGTH_COL in lines.columns else None

    # 3) Centrality factor: average betweenness of the two endpoint substations
    centrality_factor = (
        node_betweenness.get(source, 0.0) + node_betweenness.get(destination, 0.0)
    ) / 2

    reliability_rows.append({
        'Line ID': line_id,
        'Source': source,
        'Destination': destination,
        'Status': status,
        'Maintenance Factor': maintenance_factor,
        'Length (km)': length_km,
        'Centrality Factor': centrality_factor,
    })

reliability_df = pd.DataFrame(reliability_rows)

# Normalize length and centrality so they're comparable on the same scale,
# then combine into one composite score. Maintenance factor is already 0/1
# so it's left as-is (acts as a binary risk flag/weight).

if LENGTH_COL in reliability_df.columns and reliability_df[LENGTH_COL].notna().any():
    reliability_df['Length Z'] = minmax_100(reliability_df[LENGTH_COL].fillna(reliability_df[LENGTH_COL].mean()).tolist())
else:
    reliability_df['Length Z'] = 0.0

reliability_df['Centrality Z'] = minmax_100(reliability_df['Centrality Factor'].tolist())


W_MAINTENANCE = 0.5
W_LENGTH = 0.25
W_CENTRALITY = 0.25

reliability_df['Reliability Risk Score'] = (
    W_MAINTENANCE * reliability_df['Maintenance Factor']
    + W_LENGTH * reliability_df['Length Z']
    + W_CENTRALITY * reliability_df['Centrality Z']
)

reliability_df = reliability_df.sort_values('Reliability Risk Score', ascending=False)

print("Reliability Proxy Analysis (top 10 highest-risk lines):")
print("-" * 100)
print(reliability_df.head(10).to_string(index=False))

print()

# Optional: roll up to substation level — average risk score of all lines touching each substation
substation_risk = {}
for _, row in reliability_df.iterrows():
    for node in (row['Source'], row['Destination']):
        substation_risk.setdefault(node, []).append(row['Reliability Risk Score'])

substation_risk_avg = {
    node: round(sum(scores) / len(scores), 4)
    for node, scores in substation_risk.items()
}

substation_risk_ranked = dict(
    sorted(substation_risk_avg.items(), key=lambda item: item[1], reverse=True)
)

print("\nSubstation-level average reliability risk (highest first):")
print("-" * 100)
for node, score in list(substation_risk_ranked.items())[:10]:
    name = G.nodes[node].get('name', node)
    print(f"{name}: {score}")

print()
