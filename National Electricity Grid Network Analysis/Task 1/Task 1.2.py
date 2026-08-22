import pandas as pd
import statistics as stat

utilities = pd.read_csv('National Electricity Grid Network Analysis/data_files/utilities.csv') # utilities.csv
substations = pd.read_csv('National Electricity Grid Network Analysis/data_files/substations.csv') # substations.csv
lines = pd.read_csv('National Electricity Grid Network Analysis/data_files/lines.csv') # lines.csv


data = [
    ['Latitude', 'Longitude', 'Voltage (kV)', 'Capacity (MVA)', 'Commissioning Year'],
    ['Region', 'Country', 'Type', 'Status']
]

print()

for i in data[0]:
    print(f'General Statistics for "{i}":')
    print("Median:", stat.median(substations[i]))
    print("Mean:", stat.mean(substations[i]))
    print("Mode:",stat.mode(substations[i]))
    print("Min:", min(substations[i]))
    print("Max:",max(substations[i]))
    print()

# ●	Create frequency distributions for categorical variables
region_count = {}
country_count = {}
type_count = {}
status_count = {}

for i in substations[data[1][0]]:
    if i not in region_count:
        region_count[i] = 1
    else:
        region_count[i] += 1

for i in substations[data[1][1]]:
    if i not in country_count:
        country_count[i] = 1
    else:
        country_count[i] += 1

for i in substations[data[1][2]]:
    if i not in type_count:
        type_count[i] = 1
    else:
        type_count[i] += 1

for i in substations[data[1][3]]:
    if i not in status_count:
        status_count[i] = 1
    else:
        status_count[i] += 1

print("|", "="*49, "|")
print("\tSubstation Distribution Information.")
print()
print("Substation Distribution by Region: ")
for n, p in region_count.items(): # Frequency distribution for regions
    print(f"{n}: {p}")
print()

print("Substation Distribution by Country:")
for n, p in country_count.items(): # Frequency distribution for country
    print(f"{n}: {p}")
print()

print("Substation Classification by Type:")
for n, p in type_count.items(): # Frequency distribution for substation type
    print(f"{n}: {p}")
print()

print("Substation Classification by Status:")
for n, p in status_count.items(): # Frequency distribution for substation status
    print(f"{n}: {p}")
print()


print("|", "="*37, "|")
print("\tTop Facility Information.")
print()
# ●	Identify top utilities by number of lines operated
utility_ids = list(lines['Utility ID'])

utility_ids_copy = set(utility_ids)

print("→ Top utilities by no. of connected lines: ")
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

print("→ Top substations by no. of connected lines: ")
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


substation_in_region = {}
for reg in regions:
    if reg in substation_in_region:
        substation_in_region[reg] += 1
    else:
        substation_in_region[reg] = 1

regionlines = {}
for value in line_sub_ids:
    if value in sub_sub_ids:
        place = sub_sub_ids.index(value)
        region = regions[place]
        if region in regionlines:
            regionlines[region] += 1
        else:
            regionlines[region] = 1

print("|", "="*60, "|")
print("Geographic Distribution of substations and lines by Region")
print()

for reg in substation_in_region:
    numberlines = regionlines.get(reg, 0)
    print(f"Region {reg} has {substation_in_region[reg]} substations and {numberlines} lines.")

print()

# Examine voltage-level distribution
print("Voltage Summary:")
print(substations[['Voltage (kV)']].describe(), "\n")
