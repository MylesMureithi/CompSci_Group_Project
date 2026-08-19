import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import plotly.graph_objects as go
import streamlit_folium as sf
import folium
utilities = pd.read_csv('National Electricity Grid Network Analysis/data_files/utilities.csv') # utilities.csv
substations = pd.read_csv('National Electricity Grid Network Analysis/data_files/substations.csv') # substations.csv
lines = pd.read_csv('National Electricity Grid Network Analysis/data_files/lines.csv') # lines.csv


# Dashboard components:
# - Executive summary with key metrics
# - Interactive map with filtering options (region, voltage, utility)
# - Network analysis visualization
# - Business intelligence / reliability charts
# - Search functionality for specific substations/lines
# - Comparison tools for different utilities


# 1. Define your tab titles
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "📈 Network", "🌍 Geography",  "🛠️ Reliability", "🔍 Search"])

# 2. Add content to each tab using the 'with' block
with tab1:
    st.title("Dashboard Metrics")
    st.header("Key Statistics & Executive Summary")


    "### 1. High-Level Network Inventory (The Core Totals)\n"

    "Quick snapshot of the physical size of the grid we've analyzed: \n"

    "###### 1. Total Substations - The total count of electrical nodes in the substations dataset.\n"

    "###### 2. Total Transmission Lines: The total count of lines connecting the network.\n"

    "###### 3. Total Grid Capacity: The sum of all capacity_mva across the entire network, representing total apparent power handling capability.\n"

    "###### 4. Total Network Length: The sum of all ```line_length``` values, showing the total geographical footprint"



    "### 2. Operational Stress & Reliability Metrics\n"

    "These pull in the proxy analysis and density work built:\n"

    r"###### 1. High-Stress / Bottleneck Substations Count - The number (and percentage) of substations exceeding our set threshold (e.g. top 10% or $\text{Mean} + 1.5\sigma$ in $\text{MVA/kV}$ density)."

    "###### 2. Lines Under Maintenance - The total count and proportion (%) of lines currently flagged as 'Under Maintenance' relative to the whole network.\n"

    "###### 3. High-Risk Vulnerability Index - The top-tier vulnerable lines identified using your composite reliability proxy (combining maintenance status, line length, and betweenness centrality).\n"


    "### 3. Geographic & Utility Breakdown\n"

    "These summarize the footprint per region and utility:\n"

    "###### 1. Substations & Lines per Region - A breakdown of the utility footprint counts grouped by region (e.g., using ```regions = substations['Region']``` to filter).\n"

    "###### 2. Capacity Concentration Ratio - The percentage of total national/grid capacity held by the top 5% or 10% largest substations (highlighting systemic risk)."


with tab2:
    st.title("Network Overview")
    st.write("Interactive network gaphs that show connections between substations")

    regions=["All Regions"]+sorted(substations["Region"].dropna().unique().tolist())
    select_region = st.selectbox("Filter by Region",regions)
    if select_region =="All Regions": 
        substation_info=substations.copy()
    else:
        substation_info= substations[substations["Region"]==select_region]

    substation_id= set(substation_info["Substation ID"])
    lines_info=lines.copy()

    lines_info = lines[lines["Source Substation ID"].isin(substation_id)& lines["Destination Substation ID"].isin(substation_id)]

    f_metric,s_metric = st.columns(2)
    with f_metric:
        st.metric("Substations",len(substation_info))

    with s_metric:
        st.metric("Lines",len(lines_info))

    grid=nx.Graph()

    for i, substation in substation_info.iterrows():
        grid.add_node(
            substation["Substation ID"],
            name=substation["Name"],
            region=substation["Region"],
            country=substation["Country"],
            voltage = substation["Voltage (kV)"],
            capacity = substation["Capacity (MVA)"],
            status=substation["Status"]
        )

    for i,line in lines_info.iterrows():
        grid.add_edge(
            line["Source Substation ID"],
            line["Destination Substation ID"],
            line_id = line["Line ID"],
            length=line["Length (km)"],
            capacity=line["Capacity (MVA)"],
            status = line["Status"]
        )
    node_place = nx.spring_layout(grid, seed=42)
    line_xcoor=[]
    line_ycoor=[]

    for source_substation_id, destination_substation_id in grid.edges():
        source_sub_xcoor,source_sub_ycoor =node_place[source_substation_id]
        destination_sub_xcoor,destination_ycoor=node_place[destination_substation_id]

        line_xcoor.extend([source_sub_xcoor,destination_sub_xcoor,None])
        line_ycoor.extend([source_sub_ycoor,destination_ycoor,None])

    line_join = go.Scatter(
        x=line_xcoor,
        y=line_ycoor,
        mode="lines",
        line=dict(width=1),
        hoverinfo="none",
        name="Transmission Lines"
    )

    sub_xcoors=[]
    sub_ycoors=[]
    sub_hover_info=[]
    sub_marker_sides=[]

    for substation_id in grid.nodes():
        sub_xcoor,sub_ycoor=node_place[substation_id]
        sub_xcoors.append(sub_xcoor)
        sub_ycoors.append(sub_ycoor)
        substation=grid.nodes[substation_id]
        no_of_connections=grid.degree[substation_id]

        sub_hover_info.append(
            f"<b>{substation["name"]}</b><br>"
            f"Region: {substation["region"]}<br>"
            f"Country: {substation["country"]}<br>"
            f"Voltage: {substation["voltage"]}<br>"
            f"Capacity: {substation["capacity"]}MVA<br>"
            f"Voltage: {substation["voltage"]}kV<br>"
            f"Status: {substation["status"]}<br>"
            f"Connected Lines: {no_of_connections}"

        )
        sub_marker_sides.append(max(15,substation["capacity"]**0.5))

    sub_join= go.Scatter(
        x=sub_xcoors,
        y=sub_ycoors,
        mode="markers",
        text=sub_hover_info,
        hoverinfo="text",
        marker=dict(size=sub_marker_sides),
        name="Substations"
    )
    grid_figure=go.Figure(
        data=[line_join,sub_join]
    )

    grid_figure.update_layout(
        title="Key",
        title_x=0.8,
        showlegend=True,
        hovermode="closest",
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        yaxis=dict(
                        showgrid=False,
                        zeroline=False,
                        showticklabels=False
        ),
        height=800
    )

    st.plotly_chart(grid_figure,use_container_width=True)


with tab3:
    st.title("Geography Overview")
    st.checkbox("Enable Notifications")
    def geography_overview(utilities, substations, lines):

        st.header("3.1 Geography Overview")
        st.subheader("National Electricity Grid Map")

        utilities_map = utilities.copy()
        substations_map = substations.copy()
        lines_map = lines.copy()

        substations_map = substations_map.dropna(
            subset=["Latitude", "Longitude"]
        )

        substations_map["Latitude"] = pd.to_numeric(
            substations_map["Latitude"],
            errors="coerce"
        )

        substations_map["Longitude"] = pd.to_numeric(
            substations_map["Longitude"],
            errors="coerce"
        )

        substations_map = substations_map.dropna(
            subset=["Latitude", "Longitude"]
        )

        st.sidebar.subheader("Map Controls")

        regions = sorted(
            substations_map["Region"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_region = st.sidebar.selectbox(
            "Select Region",
            ["All Regions"] + regions
        )

        show_substations = st.sidebar.checkbox(
            "Show Substations",
            value=True
        )

        show_lines = st.sidebar.checkbox(
            "Show Transmission Lines",
            value=True
        )

        if selected_region != "All Regions":
            filtered_substations = substations_map[
                substations_map["Region"] == selected_region
            ]
        else:
            filtered_substations = substations_map.copy()

        visible_substation_ids = set(
            filtered_substations["Substation ID"].astype(str)
        )

        coordinate_lookup = {}

        for i, row in substations_map.iterrows():
            substation_id = str(row["Substation ID"])

            coordinate_lookup[substation_id] = (
                row["Latitude"],
                row["Longitude"]
            )

        m = folium.Map(
            location=[7.9465, -1.0232],
            zoom_start=6,
            tiles="CartoDB positron"
        )

        substations_layer = folium.FeatureGroup(
            name="Substations"
        )

        lines_layer = folium.FeatureGroup(
            name="Transmission Lines"
        )

        if show_lines:

            for _, line in lines_map.iterrows():

                source_id = str(line["Source Substation ID"])
                destination_id = str(line["Destination Substation ID"])

                if (
                    source_id not in coordinate_lookup
                    or destination_id not in coordinate_lookup
                ):
                    continue

                if selected_region != "All Regions":

                    if (
                        source_id not in visible_substation_ids
                        and destination_id not in visible_substation_ids
                    ):
                        continue

                source_coords = coordinate_lookup[source_id]
                destination_coords = coordinate_lookup[destination_id]

                line_id = line["Line ID"]
                source_name = line["Source Substation"]
                destination_name = line["Destination Substation"]
                voltage = line["Voltage (kV)"]
                length = line["Length (km)"]
                capacity = line["Capacity (MVA)"]
                status = line["Status"]
                line_type = line["Line Type"]
                utility_id = line["Utility ID"]

                utility_name = "Unknown"

                utility_match = utilities_map[
                    utilities_map["Utility ID"].astype(str)
                    == str(utility_id)
                ]

                if not utility_match.empty:
                    utility_name = utility_match.iloc[0]["Name"]

                popup_html = f"""
                <div style="font-size: 14px;">
                    <h4>Transmission Line</h4>
                    <b>Line ID:</b> {line_id}<br>
                    <b>Utility:</b> {utility_name}<br>
                    <b>From:</b> {source_name}<br>
                    <b>To:</b> {destination_name}<br>
                    <b>Voltage:</b> {voltage} kV<br>
                    <b>Length:</b> {length} km<br>
                    <b>Capacity:</b> {capacity} MVA<br>
                    <b>Status:</b> {status}<br>
                    <b>Line Type:</b> {line_type}
                </div>
                """

                folium.PolyLine(
                    locations=[source_coords,destination_coords],
                    weight=3,
                    opacity=0.8,
                    tooltip=f"{source_name} → {destination_name}",
                    popup=folium.Popup(
                        popup_html,
                        max_width=350
                    )
                ).add_to(lines_layer)

        if show_substations:

            for _, substation in filtered_substations.iterrows():

                latitude = substation["Latitude"]
                longitude = substation["Longitude"]
                name = substation["Name"]
                short_name = substation["Short Name"]
                region = substation["Region"]
                voltage = substation["Voltage (kV)"]
                capacity = substation["Capacity (MVA)"]
                commissioning_year = substation["Commissioning Year"]
                substation_type = substation["Type"]
                status = substation["Status"]

                popup_html = f"""
                <div style="font-size: 14px;">
                    <h4>Substation</h4>
                    <b>Name:</b> {name}<br>
                    <b>Short Name:</b> {short_name}<br>
                    <b>Region:</b> {region}<br>
                    <b>Voltage:</b> {voltage} kV<br>
                    <b>Capacity:</b> {capacity} MVA<br>
                    <b>Commissioned:</b> {commissioning_year}<br>
                    <b>Type:</b> {substation_type}<br>
                    <b>Status:</b> {status}
                </div>
                """

                folium.CircleMarker(
                    location=[
                        latitude,
                        longitude
                    ],
                    radius=6,
                    popup=folium.Popup(
                        popup_html,
                        max_width=350
                    ),
                    tooltip=name,
                    fill=True,
                    fill_opacity=0.9,
                    weight=2
                ).add_to(substations_layer)

        if show_lines:
            lines_layer.add_to(m)

        if show_substations:
            substations_layer.add_to(m)

        folium.LayerControl().add_to(m)

        sf.folium_static(m,width=1200,height=650)

        st.subheader("Geographical Network Summary")

        column1, column2, column3, column4 = st.columns(4)

        with column1:
            st.metric("Substations",len(filtered_substations))

        with column2:
            st.metric("Transmission Lines",len(lines_map))

        with column3:
            st.metric("Regions",filtered_substations["Region"].nunique())

        with column4:
            total_capacity = pd.to_numeric(
                filtered_substations["Capacity (MVA)"],
                errors="coerce"
            ).sum()

            st.metric("Substation Capacity",f"{total_capacity} MVA"
            )

        st.subheader("Substations in Selected Area")

        display_columns = [
            "Substation ID","Name","Region","Latitude","Longitude","Voltage (kV)","Capacity (MVA)",
            "Type","Status"
        ]

        available_columns = [column for column in display_columns if column in filtered_substations.columns]

        st.dataframe(
            filtered_substations[available_columns],
            use_container_width=True,
            hide_index=True
        )


    geography_overview(utilities,substations,lines)



with tab4:
    st.title("Reliability Overview")
    st.write("Welcome to the Reliability Overview.")

    """
    Reliability tab:
    - "business capacity and capacity/reliability analysis"
    - "Business intelligence / reliability charts"

    """

with tab5:
    st.title("Search Tab")
    st.write("Search for specific substations and lines!")

    """
    Search tab:
    - "substation finder and utility comparison tools
    - "Search functionality for specific substations/lines"
    - "Comparison tools for different utilities"
    """



# run command: python -m streamlit run "National Electricity Grid Network Analysis/Part A/Task 3/Task 3.1.py"



# Line chart
#data = pd.DataFrame(np.random.randn(20, 3), columns=["A", "B", "C"])
#st.line_chart(data)

# Map visualization
#map_data = pd.DataFrame(np.random.randn(100, 2) / [50, 50] + [37.76, -122.4], columns=["lat", "lon"])
#st.map(map_data)
