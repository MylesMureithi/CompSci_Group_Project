import pandas as pd

# The generator script already writes proper headers, so we can read directly.
utilities = pd.read_csv('National Electricity Grid Network Analysis/Part A/data_files/utilities.csv')
substations = pd.read_csv('National Electricity Grid Network Analysis/Part A/data_files/substations.csv')
lines = pd.read_csv('National Electricity Grid Network Analysis/Part A/data_files/lines.csv')

# Inspect the data
print("Utilities DataFrame Info:")
print(utilities.info(), "\n")
print("Utilities First 5 Rows:")
print(utilities.head(), "\n")

print("Substations DataFrame Info:")
print(substations.info(), "\n")
print("Substations First 5 Rows:")
print(substations.head(), "\n")

print("Lines DataFrame Info:")
print(lines.info(), "\n")
print("Lines First 5 Rows:")
print(lines.head(), "\n")