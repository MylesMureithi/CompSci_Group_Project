import pandas as pd
import statistics as stat
from datetime import datetime
import networkx as nx
import matplotlib.pyplot as plt

utilities = pd.read_csv('National Electricity Grid Network Analysis/data_files/utilities.csv') # utilities.csv
substations = pd.read_csv('National Electricity Grid Network Analysis/data_files/substations.csv') # substations.csv
lines = pd.read_csv('National Electricity Grid Network Analysis/data_files/lines.csv') # lines.csv

# Using Streamlit or Dash
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Create publication-quality visualizations
# - Animated maps showing grid expansion by Commissioning Year
# - 3D network visualizations
# - Interactive chord diagrams for inter-regional power-line flows
# - Heatmaps for line density and maintenance-status concentration
# - Comparative charts for utility infrastructure footprints