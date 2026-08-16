import folium
from geopy.distance import geodesic
import pandas as pd

utilities = pd.read_csv('National Electricity Grid Network Analysis/data_files/utilities.csv') # utilities.csv
substations = pd.read_csv('National Electricity Grid Network Analysis/data_files/substations.csv') # substations.csv
lines = pd.read_csv('National Electricity Grid Network Analysis/data_files/lines.csv') # lines.csv


# Matches every Substation ID to its latitude and longitude
substation_coordinates = (
    substations
    .set_index("Substation ID")[["Latitude", "Longitude"]]
    .apply(tuple, axis=1)
    .to_dict()
)

# Calculate the direct geographic distance for one transmission line.
def calculate_geodesic_distance(line):

    source_substation_id = line["Source Substation ID"]
    destination_substation_id = line["Destination Substation ID"]

    # If either substation is missing, the distance cannot be calculated.
    if (
        source_substation_id not in substation_coordinates
        or destination_substation_id not in substation_coordinates
    ):
        return None

    source_coordinates = substation_coordinates[source_substation_id]
    destination_coordinates = substation_coordinates[destination_substation_id]

    # geodesic() uses the two coordinate pairs.
    # .km returns the result in kilometres.
    return geodesic(
        source_coordinates,
        destination_coordinates
    ).km

# axis=1 means run the function on each row.
lines["Geodesic Distance (km)"] = lines.apply(
    calculate_geodesic_distance,
    axis=1
)

# Compare the recorded length with the calculated direct distance.
lines["Distance Difference (km)"] = (
    lines["Length (km)"]
    - lines["Geodesic Distance (km)"]
)

print(
    lines[
        [
            "Line ID",
            "Source Substation",
            "Destination Substation",
            "Length (km)",
            "Geodesic Distance (km)",
            "Distance Difference (km)"
        ]
    ]
)

# Put substations from the same region together.
regional_substation_summary = (
    substations
    .groupby("Region")
    .agg(
        Substation_Count=("Substation ID", "count"),
        Average_Capacity_MVA=("Capacity (MVA)", "mean"),
        Total_Capacity_MVA=("Capacity (MVA)", "sum")
    )
    .sort_values(
        "Substation_Count",
        ascending=False
    )
)

print(regional_substation_summary)

# I use 40 km as a simple distance for deciding whether
# another substation is geographically nearby.
nearby_distance_km = 40

# Store the number of nearby substations for every station.
nearby_substation_counts = []

# Compare each substation with every other substation.
for first_index, first_substation in substations.iterrows():

    nearby_substation_count = 0

    first_substation_coordinates = (
        first_substation["Latitude"],
        first_substation["Longitude"]
    )

    for second_index, second_substation in substations.iterrows():

        # Compare substations with other substations.
        if first_index != second_index:

            second_substation_coordinates = (
                second_substation["Latitude"],
                second_substation["Longitude"]
            )

            distance_between_substations = geodesic(
                first_substation_coordinates,
                second_substation_coordinates
            ).km

            # Count another station if it is within 40 km.
            if distance_between_substations <= nearby_distance_km:
                nearby_substation_count += 1

    nearby_substation_counts.append(nearby_substation_count)

# Add the counts to the substations DataFrame.
substations["Nearby Substations"] = nearby_substation_counts

# At least two nearby substations suggests a local concentration.
substations_in_clusters = substations[
    substations["Nearby Substations"] >= 2
]

# No nearby substations suggests geographic isolation.
possible_coverage_gaps = substations[
    substations["Nearby Substations"] == 0
]

print("\nSubstations in Geographic Concentrations")
print(
    substations_in_clusters[
        ["Name", "Region", "Nearby Substations"]
    ]
)

print("\nSeparated Substations") 
print(
    possible_coverage_gaps[
        ["Name", "Region", "Country", "Nearby Substations"]
    ]
)

# Add the utility name to every transmission line.
lines_with_utility = lines.merge(
    utilities[
        ["Utility ID", "Name"]
    ].rename(
        columns={"Name": "Utility Name"}
    ),
    on="Utility ID",
    how="left"
)

# Add source coordinates.
lines_with_geographic_data = lines_with_utility.merge(
    substations[
        ["Substation ID", "Latitude", "Longitude"]
    ].rename(
        columns={
            "Latitude": "Source Latitude",
            "Longitude": "Source Longitude"
        }
    ),
    left_on="Source Substation ID",
    right_on="Substation ID",
    how="left"
).drop(columns="Substation ID")

# Add destination coordinates.
lines_with_geographic_data = lines_with_geographic_data.merge(
    substations[
        ["Substation ID", "Latitude", "Longitude"]
    ].rename(
        columns={
            "Latitude": "Destination Latitude",
            "Longitude": "Destination Longitude"
        }
    ),
    left_on="Destination Substation ID",
    right_on="Substation ID",
    how="left"
).drop(columns="Substation ID")

# Centre used by the Folium maps.
map_center = [
    substations["Latitude"].mean(),
    substations["Longitude"].mean()
]

# FOLIUM METHOD: Map()
# Creates the interactive map.
utility_network_map = folium.Map(
    location=map_center,
    zoom_start=4
)

# Get each utility name once.
utility_names = (
    lines_with_geographic_data["Utility Name"]
    .dropna()
    .unique()
)

for utility_name in utility_names:

    # FOLIUM METHOD: FeatureGroup()
    # Creates a separate layer for one utility.
    utility_layer = folium.FeatureGroup(
        name=str(utility_name)
    )

    utility_lines = lines_with_geographic_data[
        lines_with_geographic_data["Utility Name"] == utility_name
    ]

    for  i, line in utility_lines.iterrows():

        if (
            pd.notna(line["Source Latitude"])
            and pd.notna(line["Source Longitude"])
            and pd.notna(line["Destination Latitude"])
            and pd.notna(line["Destination Longitude"])
        ):

            # FOLIUM METHOD: PolyLine()
            # Draws the transmission line between two coordinate pairs.
            folium.PolyLine(
                locations=[
                    [
                        line["Source Latitude"],
                        line["Source Longitude"]
                    ],
                    [
                        line["Destination Latitude"],
                        line["Destination Longitude"]
                    ]
                ],
                weight=2,
                tooltip=(
                    f"{utility_name}: "
                    f"{line['Source Substation']} -> "
                    f"{line['Destination Substation']}"
                )
            ).add_to(utility_layer)

    # Places the completed utility layer on the map.
    utility_layer.add_to(utility_network_map)

# FOLIUM METHOD: LayerControl()
folium.LayerControl().add_to(utility_network_map)

utility_network_map.save("utility_line_networks.html")
# Give each voltage level a colour.
voltage_level_colors = {
    11: "green",
    33: "blue",
    69: "purple",
    161: "orange",
    330: "red"
}

# FOLIUM METHOD: Map()
national_substation_map = folium.Map(
    location=map_center,
    zoom_start=4
)

for i, substation in substations.iterrows():

    # If a voltage is not in the dictionary, use grey.
    voltage_color = voltage_level_colors.get(substation["Voltage (kV)"],"gray")

    # FOLIUM METHOD: CircleMarker()
    # Places a circle at the substation's real coordinates.
    folium.CircleMarker(
        location=[substation["Latitude"],substation["Longitude"] ],

        # radius controls marker size.
        radius=5,

        # color controls the outside of the circle.
        color=voltage_color,

        # fill=True fills the marker.
        fill=True,

        # fill_color controls the inside colour.
        fill_color=voltage_color,

        # popup appears when the marker is clicked.
        popup=(
            f"Name: {substation['Name']}<br>"
            f"Region: {substation['Region']}<br>"
            f"Voltage: {substation['Voltage (kV)']} kV<br>"
            f"Capacity: {substation['Capacity (MVA)']} MVA<br>"
            f"Status: {substation['Status']}"
        ),

        # tooltip appears when I hover over the marker.
        tooltip=substation["Name"]

    # add_to() places the marker on this map.
    ).add_to(national_substation_map)

national_substation_map.save(
    "national_substations_by_voltage.html"
)


# Count how many transmission lines connect to each substation.
connected_line_counts = {}

for i, line in lines.iterrows():

    source_substation_id = line["Source Substation ID"]
    destination_substation_id = line["Destination Substation ID"]

    connected_line_counts[source_substation_id] = (
        connected_line_counts.get(source_substation_id, 0) + 1
    )

    connected_line_counts[destination_substation_id] = (
        connected_line_counts.get(destination_substation_id, 0) + 1
    )

# Match each Substation ID to its number of connected lines.
substations["Connected Lines"] = (
    substations["Substation ID"]
    .map(connected_line_counts)
    .fillna(0)
)

# FOLIUM METHOD: Map()
line_density_map = folium.Map(
    location=map_center,
    zoom_start=4
)

for i, substation in substations.iterrows():

    number_of_connected_lines = substation["Connected Lines"]

    # Larger circles mean more connected transmission lines.
    marker_radius = 4 + number_of_connected_lines

    # FOLIUM METHOD: CircleMarker()
    folium.CircleMarker(
        location=[
            substation["Latitude"],
            substation["Longitude"]
        ],
        radius=marker_radius,
        fill=True,
        popup=(
            f"Substation: {substation['Name']}<br>"
            f"Connected Lines: {number_of_connected_lines}"
        ),
        tooltip=substation["Name"]
    ).add_to(line_density_map)

line_density_map.save(
    "line_density_concentration_map.html"
)


# Match each Substation ID to its region and country.
substation_region_lookup = (
    substations
    .set_index("Substation ID")["Region"]
    .to_dict()
)

substation_country_lookup = (
    substations
    .set_index("Substation ID")["Country"]
    .to_dict()
)

lines_with_geographic_data["Source Region"] = (
    lines_with_geographic_data["Source Substation ID"]
    .map(substation_region_lookup)
)

lines_with_geographic_data["Destination Region"] = (
    lines_with_geographic_data["Destination Substation ID"]
    .map(substation_region_lookup)
)

lines_with_geographic_data["Source Country"] = (
    lines_with_geographic_data["Source Substation ID"]
    .map(substation_country_lookup)
)

lines_with_geographic_data["Destination Country"] = (
    lines_with_geographic_data["Destination Substation ID"]
    .map(substation_country_lookup)
)

connectivity_types = []

for i, line in lines_with_geographic_data.iterrows():

    if (
        line["Source Country"]
        != line["Destination Country"]
    ):
        connectivity_types.append("Cross-border")

    elif (
        line["Source Region"]
        != line["Destination Region"]
    ):
        connectivity_types.append("Inter-regional")

    else:
        connectivity_types.append("Intra-regional")

lines_with_geographic_data["Connectivity Type"] = (
    connectivity_types
)

connectivity_summary = (
    lines_with_geographic_data["Connectivity Type"]
    .value_counts()
)

print(connectivity_summary)

# FOLIUM METHOD: Map()
regional_connectivity_map = folium.Map(
    location=map_center,
    zoom_start=4
)

for i, line in lines_with_geographic_data.iterrows():

    if (
        pd.notna(line["Source Latitude"])
        and pd.notna(line["Source Longitude"])
        and pd.notna(line["Destination Latitude"])
        and pd.notna(line["Destination Longitude"])
    ):

        connectivity_type = line["Connectivity Type"]

        if connectivity_type == "Cross-border":
            connectivity_color = "red"
        elif connectivity_type == "Inter-regional":
            connectivity_color = "blue"
        else:
            connectivity_color = "gray"

        # FOLIUM METHOD: PolyLine()
        folium.PolyLine(
            locations=[
                [
                    line["Source Latitude"],
                    line["Source Longitude"]
                ],
                [
                    line["Destination Latitude"],
                    line["Destination Longitude"]
                ]
            ],
            color=connectivity_color,
            weight=2,
            tooltip=(
                f"{connectivity_type}: "
                f"{line['Source Substation']} "
                f"{line['Destination Substation']}"
            )
        ).add_to(regional_connectivity_map)

        regional_connectivity_map.save(
    "regional_cross_border_connectivity.html"
)
