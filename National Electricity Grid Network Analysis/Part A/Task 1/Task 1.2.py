import pandas as pd
import numpy as np
import statistics as stat
import matplotlib.pyplot as plt


utilities = pd.read_csv('National Electricity Grid Network Analysis/data_files/utilities.csv') # utilities.csv
substations = pd.read_csv('National Electricity Grid Network Analysis/data_files/substations.csv') # substations.csv
lines = pd.read_csv('National Electricity Grid Network Analysis/data_files/lines.csv') # lines.csv

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

"""



"""for i in data[0]:
    for j, value in enumerate(substations[i]):
        if type(value) in types:
            continue
        else:
            print("Not In Types")"""

"""Objective: Understand dataset characteristics and identify initial patterns
Specific Activities:
●	Generate descriptive statistics for all numerical variables
●	Create frequency distributions for categorical variables
●	Identify top utilities by number of lines operated
●	Find the most-connected substations by number of lines
●	Analyse geographic distribution of substations and lines by region
●	Examine substation status (Active/Inactive) and voltage-level distribution
"""

data = [
    ['Latitude', 'Longitude', 'Voltage (kV)', 'Capacity (MVA)', 'Commissioning Year'],
    ['Name', 'Region', 'Country', 'Type', 'Status']
]

print()

for i in data[0]:
    print(f"{i}:")
    print("Median:", stat.median(substations[i]))
    print("Mean:", stat.mean(substations[i]))
    print("Mode:",stat.mode(substations[i]))
    print("Min:", min(substations[i]))
    print("Max:",max(substations[i]))
    print()

# ●	Create frequency distributions for categorical variables
counted = {}

for i in data[1]:
    for j in substations[i]:
        count = 1

        if j not in counted:
            counted[j] = count
        else:
            counted[j] = count + 1

for n, p in counted.items():
    print(f"{n}: {p}")
print()


# ●	Identify top utilities by number of lines operated
utility_ids = list(lines['Utility ID'])

utility_ids_copy = set(utility_ids)

for value in utility_ids_copy:
    if value in utility_ids:
        count = utility_ids.count(value)

        if count == 1:
            continue
        else:
            print(f"Utility ID {value} appears {count} times.")

print()

# ●	Find the most-connected substations by number of lines
sub_ids = list(lines['Source Substation ID'])

sub_ids_copy = set(sub_ids)

for value in sub_ids_copy:
    if value in sub_ids:
        count = sub_ids.count(value)

        if count == 1:
            continue
        else:
            print(f"Source Substation ID {value} connects to {count} lines.")

print()

# ●	Analyse geographic distribution of substations and lines by [region] substation ID

regions = substations['Region']
line_sub_ids = list(lines['Source Substation ID'])
sub_sub_ids = list(substations['Substation ID'])


"""for value in line_sub_ids:
    if value in sub_sub_ids:
        print(regions[value])"""
"""for value in line_sub_ids:
    if value in sub_sub_ids:
        line_count = line_sub_ids.count(value)
        print(value, line_count)"""

# Did some research and for what we are dealing with I think we can use the Counter from python collections. Just a thought though.
#From collections import Counter

"""sub_ids = list(lines['Source Substation ID'])

sub_ids_copy = set(sub_ids)

for value in sub_ids_copy:
    if value in sub_ids:
        count = sub_ids.count(value)

        if count == 1:
            continue
        else:
            print(f"Source Substation ID {value} connects to {count} lines.")

print()


for value in line_ids_copy:
    if value in line_ids:
        count = line_ids.count(value)

        if count == 1:
            continue
        else:
            print(f"ID {value} is duplicated {count} times.")"""


substationinregion={}
for reg in regions:
    if reg in substationinregion:
        substationinregion[reg] = substationinregion[reg] + 1
    else:
        substationinregion[reg] = 1

regionlines={}
for value in line_sub_ids:
    if value in sub_sub_ids:
        place = sub_sub_ids.index(value)
        region = regions[place]
        if region in regionlines:
            regionlines[region] = regionlines[region] + 1
        else:
            regionlines[region] = 1


for reg in substationinregion:
    numberlines =regionlines.get(reg, 0)
    print(f"Region {reg} has {substationinregion[reg]} substations and {numberlines} lines.")

"""Examine substation status (Active/Inactive) and voltage-level distribution"""
print()
print("Substation Status Analysis:")
print(substations['Status'].value_counts(), "\n")

print("Voltage Summary:")
print(substations[[ 'Voltage (kV)']].describe(), "\n")
