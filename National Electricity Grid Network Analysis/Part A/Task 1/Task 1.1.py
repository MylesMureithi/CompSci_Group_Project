# Step 1: Load and examine raw data

import pandas as pd
import numpy as np
import statistics as stat


utilities = pd.read_csv('National Electricity Grid Network Analysis/Part A/data_files/utilities.csv') # utilities.csv
substations = pd.read_csv('National Electricity Grid Network Analysis/Part A/data_files/substations.csv') # substations.csv
lines = pd.read_csv('National Electricity Grid Network Analysis/Part A/data_files/lines.csv') # lines.csv


median_lat = stat.median(substations['Latitude'])
print("Median Latitude:", median_lat)

median_long = stat.median(substations['Longitude'])
print("Median Longitude:", median_long)

median_volt = stat.median(substations['Voltage (kV)'])
print("Median Voltage:", median_volt)

median_cap = stat.median(substations['Capacity (MVA)'])
print("Median Capacity:", round(median_cap, 2))
print()



data = [
    ['Latitude', 'Longitude', 'Voltage (kV)', 'Capacity (MVA)', 'Commissioning Year'],
    [median_lat, median_long, median_volt, median_cap]
]

k = 0

for i in data[0]:
    for j, value in enumerate(substations[i]):
        if pd.isna(value) == True:
            substations.loc[j, i] = data[1][k]

            k = k + 1

            substations.to_csv("new_substations.csv", index=False)



line_ids = list(lines['Source Substation ID'])
sub_ids = list(substations['Substation ID'])

present = 0
not_present = 0

for value in line_ids:
    if value in sub_ids:
        present += 1
    else:
        not_present +=1


line_ids_copy = set(line_ids)

for value in line_ids_copy:
    if value in line_ids:
        count = line_ids.count(value)

        if count == 1:
            continue
        else:
            print(f"ID {value} is duplicated {count} times.")


print(f"\nPresent values: {present}")
print(f"Not present values: {not_present}")

print()

min_lat = 4
max_lat = 28

min_long = -17
max_long = 16

longitudes = substations['Longitude']
latitudes = substations['Latitude']

for val in longitudes:
    if min_long <= val <= max_long:
        print("Valid Longitude")
    else:
        print("Invalid Longitude")

print()

for val in latitudes:
    if min_lat <= val <= max_lat:
        print("Valid Latitude")
    else:
        print("Invalid Latitude")

print()

types = [int, float]

for i in data[0]:
    for j, value in enumerate(substations[i]):
        if type(value) in types:
            continue
        else:
            print("Not In Types")

