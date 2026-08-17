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


# Dashboard components:
# - Executive summary with key metrics
# - Interactive map with filtering options (region, voltage, utility)
# - Network analysis visualization
# - Business intelligence / reliability charts
# - Search functionality for specific substations/lines
# - Comparison tools for different utilities