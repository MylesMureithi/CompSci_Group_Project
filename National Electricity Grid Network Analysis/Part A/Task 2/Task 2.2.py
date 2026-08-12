import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import statistics as stat


import folium
from geopy.distance import geodesic

import geopandas as gp
import geodatasets as gd


utilities = pd.read_csv('National Electricity Grid Network Analysis/data_files/utilities.csv') # utilities.csv
substations = pd.read_csv('National Electricity Grid Network Analysis/data_files/substations.csv') # substations.csv
lines = pd.read_csv('National Electricity Grid Network Analysis/data_files/lines.csv') # lines.csv


## Geographic analysis
# - Recompute (or verify) line distances using the geodesic/haversine formula
sub_longitudes = list(substations['Longitude'])
sub_latitudes = list(substations['Latitude'])
locations = list(substations['Name'])

location_coords = {}
clustered = {}
gaps = {}


mean_distance = stat.mean(lines['Length (km)'])

for loc, lat, long in zip(locations, sub_latitudes, sub_longitudes):
    location_coords[loc] = (lat, long)

line_locations = list(zip(lines['Source Substation'], lines['Destination Substation']))

for source, destination in line_locations:
    source_coords = location_coords[source]
    destination_coords = location_coords[destination]

    distance = geodesic(source_coords, destination_coords).km

    print(f"{source} to {destination} = {distance:.3f}km")

    if distance <= mean_distance:
        clustered[source] = f"{distance:.3f}"
    elif distance > (2*mean_distance):
        gaps[source] = f"{distance:.3f}"





# - Analyse substation density by region
regions = substations['Region']
line_sub_ids = list(lines['Source Substation ID'])
sub_sub_ids = list(substations['Substation ID'])

substationinregion = {}
for reg in regions:
    if reg in substationinregion:
        substationinregion[reg] = substationinregion[reg] + 1
    else:
        substationinregion[reg] = 1

regionlines = {}
for value in line_sub_ids:
    if value in sub_sub_ids:
        place = sub_sub_ids.index(value)
        region = regions[place]
        if region in regionlines:
            regionlines[region] = regionlines[region] + 1
        else:
            regionlines[region] = 1


for reg in substationinregion:
    numberlines = regionlines.get(reg, 0)
    print(f"Region {reg} has {substationinregion[reg]} substations.")

print()

# - Identify geographic clusters and coverage gaps
print(clustered)
print()
print(gaps)

# - Map each utility's line network
min_lat, max_lat = 37, 34
min_lon, max_lon = 17, 51

m = folium.Map(
    max_bounds=True,
    location=[-20, -40],
    zoom_start=6,
    min_lon=min_lon,
    max_lon=max_lon,
    min_lat=min_lat,
    max_lat=max_lat,
   
    
)

folium.CircleMarker([max_lat, min_lon], tooltip="Upper Left Corner").add_to(m)
folium.CircleMarker([min_lat, min_lon], tooltip="Lower Left Corner").add_to(m)
folium.CircleMarker([min_lat, max_lon], tooltip="Lower Right Corner").add_to(m)
folium.CircleMarker([max_lat, max_lon], tooltip="Upper Right Corner").add_to(m)

m.save("m.html")


# - Utility-specific network maps
# - Regional and cross-border connectivity analysis