# Step 1: Load and examine raw data

import pandas as pd
import numpy as np
import statistics as stat
import time


utilities = pd.read_csv('National Electricity Grid Network Analysis/data_files/utilities.csv') # utilities.csv
substations = pd.read_csv('National Electricity Grid Network Analysis/data_files/substations.csv') # substations.csv
lines = pd.read_csv('National Electricity Grid Network Analysis/data_files/lines.csv') # lines.csv

print() # Stopgap for the next section

print("General Statistics: ")
time.sleep(.5)
median_lat = stat.median(substations['Latitude'])
print("Median Latitude:", median_lat)

median_long = stat.median(substations['Longitude'])
print("Median Longitude:", median_long)

median_volt = stat.median(substations['Voltage (kV)'])
print("Median Voltage:", median_volt)

median_cap = stat.median(substations['Capacity (MVA)'])
print("Median Capacity:", round(median_cap, 2))


print() # Stopgap for the next section


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

time.sleep(.5)
print("Cross-checking 'Source Substation ID' in `lines.csv` with 'Substation ID' in `substations.csv`...")
time.sleep(1.3)

print(f"Present IDs : {present}")
print(f"Absent IDs: {not_present}")

print()


line_ids_copy = set(line_ids)

time.sleep(.5)

print("Checking for duplicate entries...")
for value in line_ids_copy:
    if value in line_ids:
        count = line_ids.count(value)

        if count == 1:
            continue
        else:
            print(f"ID {value} is duplicated {count} times.")

time.sleep(1)
print("All other ID values aren't duplicated.")

print()

min_lat = 4
max_lat = 28

min_long = -17
max_long = 16

longitudes = substations['Longitude']
latitudes = substations['Latitude']

time.sleep(.7)
print("Checking longitude validity...")
time.sleep(1.3)

for i, val in enumerate(longitudes):
    if min_long <= val <= max_long:
        print(f"{i+1}: Valid Longitude.")
    else:
        print(f"{i+1}: Invalid Longitude.")

print()

time.sleep(.7)
print("Checking latitude validity...")
time.sleep(1)

for i, val in enumerate(latitudes):
    if min_lat <= val <= max_lat:
        print(f"{i+1}: Valid Latitude.")
    else:
        print(f"{i+1}: Invalid Latitude.")

print()

types = [int, float]

time.sleep(.7)
print("Checking type validity...")
time.sleep(1)

for i in data[0]:
    for j, value in enumerate(substations[i]):
        if type(value) in types:
            print(f"{j+1}: {value} has a valid type [{type(value)}].")
        else:
            print(f"{j+1}: {value} has an invalid type [{type(value)}].")

print()