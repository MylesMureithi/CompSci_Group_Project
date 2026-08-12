import pandas as pd

# The generator script already writes proper headers, so we can read directly.
utilities = pd.read_csv('National Electricity Grid Network Analysis/data_files/utilities.csv') # utilities.csv
substations = pd.read_csv('National Electricity Grid Network Analysis/data_files/substations.csv') # substations.csv
lines = pd.read_csv('National Electricity Grid Network Analysis/data_files/lines.csv') # lines.csv

# Check for missing values
print("Missing Values in Utilities:")
print(utilities.isnull().sum(), "\n")
print("Missing Values in Substations:")
print(substations.isnull().sum(), "\n")
print("Missing Values in Lines:")
print(lines.isnull().sum(), "\n")

# Convert numeric columns to appropriate types
substations['Latitude'] = pd.to_numeric(substations['Latitude'], errors='coerce')
substations['Longitude'] = pd.to_numeric(substations['Longitude'], errors='coerce')
substations['Capacity (MVA)'] = pd.to_numeric(substations['Capacity (MVA)'], errors='coerce')
lines['Length (km)'] = pd.to_numeric(lines['Length (km)'], errors='coerce')

# Check for duplicates
print("Duplicate Rows in Utilities:", utilities.duplicated().sum())
print("Duplicate Rows in Substations:", substations.duplicated().sum())
print("Duplicate Rows in Lines:", lines.duplicated().sum())

# Drop duplicates if any
utilities = utilities.drop_duplicates()
substations = substations.drop_duplicates()
lines = lines.drop_duplicates()

# Verify data types and missing values after cleaning
print("\nAfter Cleaning - Substations Info:")
print(substations.info(), "\n")