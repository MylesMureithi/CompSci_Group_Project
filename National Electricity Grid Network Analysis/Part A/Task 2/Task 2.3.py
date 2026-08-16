import pandas as pd
import statistics as stat

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

#print(subs_util_alias) reveals 6 "Unknown" substations due to mismatching 'Country' names in Utilities.

for util, lines, subs in zip(line_util_alias.keys(), line_util_alias.values(), subs_util_alias.values()):
    print(f"Utility {util} has {subs} substations and {lines} lines.")

print()

# - Identify substations operating close to rated capacity (upgrade candidates)
voltage = list(substations['Voltage (kV)'])
capacity = list(substations['Capacity (MVA)'])
sub_names = list(substations['Name'])

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


# - Identify underserved regions with growth potential


# - Calculate a simple technical-loss proxy using line length and voltage
# - Analyse utility asset age using Commissioning Year
 
# Reliability metrics
# - Proportion of lines 'Under Maintenance' by region/utility
# - Substation age distribution (older assets, higher fault-risk proxy)
# - Concentration of capacity in a small number of substations (risk indicator)