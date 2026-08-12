'''
Create a master dataset by joining all three tables
# Establish foreign key relationships (Utility ID, Substation ID)
# Handle orphaned records (lines referencing a substation ID that doesn't exist)
# Create lookup dictionaries for efficient querying
# Validate join operations and document any data loss
# '''

import pandas as pd
import numpy as np
import statistics as stat
import matplotlib.pyplot as plt

utilities = pd.read_csv('National Electricity Grid Network Analysis/Part A/data_files/utilities.csv') # utilities.csv
substations = pd.read_csv('National Electricity Grid Network Analysis/Part A/data_files/substations.csv') # substations.csv
lines = pd.read_csv('National Electricity Grid Network Analysis/Part A/data_files/lines.csv') # lines.csv

"""lines_with_source = lines.merge(
    substations[['Substation ID', 'Name', 'Region', 'Country']],
    left_on='Source Substation ID', right_on='Substation ID',
    how='left', suffixes=("", '_source')
)

print(lines_with_source)

master_set = lines.merge(
    substations, on="Substation ID", how='left'
    ).merge(utilities, on="Utility ID", how='left'
)

print(master_set)
"""




# Chain merge: Orders + Customers, then + Payments
"""
master_df = df_orders.merge(
    df_customers, on="customer_id", how="left"
).merge(df_payments, on="order_id", how="left")

print(master_df.head())
"""

lines_with_source=lines.merge(substations[
    ["Substation ID","Name","Region","Country"]
], left_on="Source Substation ID" ,right_on="Substation ID",how="left")

lines_with_source=lines_with_source.rename(
    columns={
        "Name": "Source Substation Name",
        "Region": "Source Region",
        "Country": "Source Country"
}
)
lines_with_source=lines_with_source.drop( columns =["Substation ID"])

lines_with_source_and_destination_information = (
    lines_with_source.merge(
        substations[
            [
                "Substation ID",
                "Name",
                "Region",
                "Country"
            ]
        ],
        left_on="Destination Substation ID",
        right_on="Substation ID",
        how="left"
    )
)

lines_with_source_and_destination_information = (
    lines_with_source_and_destination_information.rename(
        columns={
            "Name": "Destination Substation Name",
            "Region": "Destination Region",
            "Country": "Destination Country"
        }
    )
)

lines_with_source_and_destination_information = (
    lines_with_source_and_destination_information.drop(
        columns=["Substation ID"]
    )
)

master_set = (
    lines_with_source_and_destination_information.merge(
        utilities[
            [
                "Utility ID",
                "Name",
                "Alias",
                "Code",
                "Type",
                "Country",
                "Active"
            ]
        ],
        on="Utility ID",
        how="left"
    )
)

master_set = master_set.rename(
    columns={
        "Name": "Utility Name",
        "Type": "Utility Type",
        "Country": "Utility Country",
        "Active": "Utility Active"
    }
)
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows",None)
print(master_set)


# Handle orphaned records (lines referencing a substation ID that doesn't exist)

line_sub_ids = list(lines['Source Substation ID'])
sub_sub_ids = list(substations['Substation ID'])

print(sub_sub_ids)

print()

for value in line_sub_ids:
    if value not in sub_sub_ids:
        print(f"{value} is an orphan.")
    else:
        print(f"{value} is attached!")

print()

# Create lookup dictionaries for efficient querying

# Dict 1: Substation ID: [Name, Region]
sub_names = list(substations['Name'])
sub_regions = substations['Region']

substations_dict = {}

for id in sub_sub_ids:
    substations_dict[id] = [sub_names[id - 1], sub_regions[id-1]]

# Dict 2: Line ID: [Source Substation, Destination Substation ID, Status]
line_ids = list(lines['Line ID'])
lines_substation = list(lines['Source Substation'])
destination_sub_id = list(lines['Destination Substation ID'])
line_status = list(lines['Status'])

lines_dict = {}

for id in line_ids:
    lines_dict[id] = [lines_substation[id - 1], destination_sub_id[id - 1], line_status[id - 1]]

print()

# Dict 3: Utility ID: [Name, Code, Active]
utility_id = list(utilities['Utility ID'])
utility_name = list(utilities['Name'])
utility_code = list(utilities['Code'])
utility_status = list(utilities['Active'])

utility_dict = {}

for id in utility_id:
    utility_dict[id] = [utility_name[id - 1], utility_code[id - 1], utility_status[id - 1]]

print(utility_dict)

# Validate join operations and document any data loss
