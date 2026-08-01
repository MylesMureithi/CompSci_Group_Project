''' Create a master dataset by joining all three tables
# Establish foreign key relationships (Utility ID, Substation ID)
# Handle orphaned records (lines referencing a substation ID that doesn't exist)
# Create lookup dictionaries for efficient querying
# Validate join operations and document any data loss'''

import pandas as pd
import numpy as np
import statistics as stat
import matplotlib.pyplot as plt

