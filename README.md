# Integrated Data Science and Software Engineering Course Project.


## Part 1: National Electricity Grid Network Analysis & GridCare System

A Python-based project combining **electricity-grid data analysis, network reliability analysis, interactive visualization, and GridCare-Lite**, a desktop grid-management application.

## Features

* Electricity-grid data cleaning and analysis
* Network/graph-based reliability analysis
* Centrality, PageRank, bridge and community analysis
* Risk and critical-infrastructure assessment
* Interactive Streamlit dashboards
* Geographic visualization with Folium
* Outage and maintenance management
* Customer complaints and work orders
* Multi-role authentication
* SQLite database

## Technologies

**Python · Pandas · NumPy · NetworkX · Matplotlib · Folium · Streamlit · Plotly · GeoPy · SQLite**

## Project Structure

```text
system-files/
├── main.py
├── gridcare.db
├── README.md
└── grid-analysis/
    ├── data_files/
    │   ├── utilities.csv
    │   ├── substations.csv
    │   └── lines.csv
    ├── Task 1/
    │   └── task1.py
    ├── Task 2/
    │   └── task2.py
    └── Task 3/
        ├── Task 3.1.py
        └── Task 3.2.py
```

## Tasks

### Task 1 — Data Exploration & Cleaning

Cleans and validates the grid datasets, including missing values, duplicates, coordinates, relationships, utilities, substations, and transmission lines.

```bash
python "grid-analysis/Task 1/task1.py"
```

### Task 2 — Network Science & Reliability

Models the grid as a NetworkX graph and analyzes:

* Degree, betweenness and closeness centrality
* PageRank
* Bridges and connectivity
* Communities
* Critical infrastructure
* Risk scoring

```bash
python "grid-analysis/Task 2/task2.py"
```

### Task 3.1 — Core Grid Explorer

Interactive Streamlit dashboard featuring KPIs, regional filtering, maps, infrastructure search, reliability metrics, and network statistics.

```bash
python -m streamlit run "grid-analysis/Task 3/Task 3.1.py"
```

### Task 3.2 — Advanced Analytics

Provides advanced network and geographic visualizations, including topology graphs, 3D representations, spatial networks, chord diagrams, maintenance heatmaps, and historical expansion.

```bash
python -m streamlit run "grid-analysis/Task 3/Task 3.2.py"
```

## GridCare-Lite

`main.py` launches the operational grid-management application.

Features include:

* Administrator, technician and customer-service roles
* Authentication
* Outage tracking
* Work-order assignment
* Maintenance management
* Customer complaints
* Operational reporting

```bash
python main.py
```

The application uses `gridcare.db` as its local SQLite database.

### Default Test Accounts

```text
Administrator
Username: admin
Password: password123

Technician
Username: tech1
Password: password123
```

> These credentials are for development/testing only. Change them before production use.

## Setup

Requires **Python 3.x**.

Install dependencies:

```bash
pip install pandas networkx matplotlib folium streamlit streamlit-folium plotly geopy numpy
```

Ensure the following datasets exist:

```text
grid-analysis/data_files/
├── utilities.csv
├── substations.csv
└── lines.csv
```

Run the project from the **root directory**.

## Workflow

```text
Raw Grid Data
     ↓
Task 1: Data Cleaning
     ↓
Task 2: Network & Reliability Analysis
     ↓
 ┌───────────────┬────────────────┐
 ↓               ↓
Task 3.1       Task 3.2
Core Dashboard Advanced Analytics
```

## Security

For production deployment:

* Change default passwords
* Never commit credentials
* Use secure password hashing
* Protect the SQLite database
* Validate user input
* Use proper authentication/authorization
* Store sensitive configuration securely

---

**Built with Python • Pandas • NetworkX • Matplotlib • Folium • Streamlit • Plotly • GeoPy • SQLite**
