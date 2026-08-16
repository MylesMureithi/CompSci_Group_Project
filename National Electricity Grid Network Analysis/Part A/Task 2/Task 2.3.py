import pandas as pd

utilities = pd.read_csv('National Electricity Grid Network Analysis/data_files/utilities.csv') # utilities.csv
substations = pd.read_csv('National Electricity Grid Network Analysis/data_files/substations.csv') # substations.csv
lines = pd.read_csv('National Electricity Grid Network Analysis/data_files/lines.csv') # lines.csv


# Load and capacity analysis
# - Utility footprint by number of substations and lines, per region

regions = substations['Region']
line_sub_ids = list(lines['Source Substation ID'])
sub_sub_ids = list(substations['Substation ID'])
utility_ali = list(utilities['Alias'])

line_utility_ids = list(lines['Utility ID'])

dict1 = {}

for id in line_utility_ids:
    alias = utility_ali[id - 1]
    
    if alias in dict1:
        dict1[alias] += 1
    else:
        dict1[alias] = 1

print(dict1)

"""for id in utility_ids:
    if id in substationinregion:
        utility_ali[substationinregion[utility_ids[id]]] = substationinregion[id] + 1
    else:
        substationinregion[id] = 1

print(substationinregion)"""

regionlines={}
for value in line_sub_ids:
    if value in sub_sub_ids:
        place = sub_sub_ids.index(value)
        region = regions[place]
        if region in regionlines:
            regionlines[region] = regionlines[region] + 1
        else:
            regionlines[region] = 1


"""for reg in substationinregion:
    numberlines =regionlines.get(reg, 0)
    print(f"Region {reg} has {substationinregion[reg]} substations and {numberlines} lines.")"""


# - Identify substations operating close to rated capacity (upgrade candidates)
# - Identify underserved regions with growth potential
# - Calculate a simple technical-loss proxy using line length and voltage
# - Analyse utility asset age using Commissioning Year
 
# Reliability metrics
# - Proportion of lines 'Under Maintenance' by region/utility
# - Substation age distribution (older assets, higher fault-risk proxy)
# - Concentration of capacity in a small number of substations (risk indicator)