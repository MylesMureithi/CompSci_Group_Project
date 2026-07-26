# Step 1: Load and examine raw data

import pandas as pd
import numpy as np
import statistics as stat


utilities = pd.read_csv('utilities.csv') # utilities.csv
substations = pd.read_csv('substations.csv') # substations.csv
lines = pd.read_csv('lines.csv') # lines.csv

"""
print(utilities.isna().sum())
print()

print(substations.isna().sum())
print()

print(lines.isna().sum())
print()
"""

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
    ['Latitude', 'Longitude', 'Voltage (kV)', 'Capacity (MVA)'],
    [median_lat, median_long, median_volt, median_cap]
]

k = 0

for i in data[0]:
    for j, value in enumerate(substations[i]):
        if pd.isna(value) == True:
            substations.loc[j, i] = data[1][k]

            k = k + 1

            substations.to_csv("new_substations.csv", index=False)


# Step 3: Data validation
    # Verify every Source/Destination Substation ID in lines.csv exists in substations.csv
    # Check for duplicate entries
    # Validate that latitude/longitude fall within plausible West African bounds
    # Ensure data type consistency (numeric columns are truly numeric)