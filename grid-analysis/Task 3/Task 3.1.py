import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import streamlit_folium as sf
import folium
import plotly.express as px

utilities = pd.read_csv('grid-analysis/data_files/utilities.csv') # utilities.csv
substations = pd.read_csv('grid-analysis/data_files/substations.csv') # substations.csv
lines = pd.read_csv('grid-analysis/data_files/lines.csv') # lines.csv


# Dashboard components:
# - Executive summary with key metrics
# - Interactive map with filtering options (region, voltage, utility)
# - Network analysis visualization
# - Business intelligence / reliability charts
# - Search functionality for specific substations/lines
# - Comparison tools for different utilities


# Set page configuration
st.set_page_config(
    page_title="National Electricity Grid Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Defining tab titles
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "📈 Network", "🌍 Geography",  "🛠️ Reliability", "🔍 Search"])

# Adding tab content
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

    regions = ["All Regions"]+sorted(substations["Region"].dropna().unique().tolist())
    select_region = st.selectbox("Filter by Region",regions)
    if select_region =="All Regions": 
        substation_info=substations.copy()
    else:
        substation_info = substations[substations["Region"]==select_region]

    substation_id = set(substation_info["Substation ID"])
    lines_info = lines.copy()

    lines_info = lines[lines["Source Substation ID"].isin(substation_id)& lines["Destination Substation ID"].isin(substation_id)]

    f_metric,s_metric = st.columns(2)

    with f_metric:
        st.metric("Substations",len(substation_info))

    with s_metric:
        st.metric("Lines",len(lines_info))

    grid = nx.Graph()

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
    line_xcoor = []
    line_ycoor = []

    for source_substation_id, destination_substation_id in grid.edges():
        source_sub_xcoor,source_sub_ycoor = node_place[source_substation_id]
        destination_sub_xcoor,destination_ycoor = node_place[destination_substation_id]

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

    sub_xcoors = []
    sub_ycoors = []
    sub_hover_info = []
    sub_marker_sides = []

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

    sub_join = go.Scatter(
        x=sub_xcoors,
        y=sub_ycoors,
        mode="markers",
        text=sub_hover_info,
        hoverinfo="text",
        marker=dict(size=sub_marker_sides),
        name="Substations"
    )
    grid_figure = go.Figure(
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

    with tab4:
        st.title("Reliability & Capacity Analysis")
        st.write("Business intelligence analysis of grid capacity, infrastructure status, maintenance, and reliability indicators.")
        reliability_substations=substations.copy()
        reliability_lines=lines.copy()
        reliability_utilities=utilities.copy()
        reliability_substations["Capacity (MVA)"]=pd.to_numeric(reliability_substations["Capacity (MVA)"],errors="coerce")
        reliability_substations["Voltage (kV)"]=pd.to_numeric(reliability_substations["Voltage (kV)"],errors="coerce")
        reliability_lines["Capacity (MVA)"]=pd.to_numeric(reliability_lines["Capacity (MVA)"],errors="coerce")
        reliability_lines["Length (km)"]=pd.to_numeric(reliability_lines["Length (km)"],errors="coerce")
        reliability_substations["Capacity (MVA)"]=reliability_substations["Capacity (MVA)"].fillna(0)
        reliability_lines["Capacity (MVA)"]=reliability_lines["Capacity (MVA)"].fillna(0)
        reliability_lines["Length (km)"]=reliability_lines["Length (km)"].fillna(0)

        st.subheader("Key Reliability Indicators")
        total_capacity=reliability_substations["Capacity (MVA)"].sum()
        total_substations=len(reliability_substations)
        total_lines=len(reliability_lines)
        maintenance_lines=reliability_lines[reliability_lines["Status"].astype(str).str.lower().str.contains("maintenance")]
        maintenance_percentage=len(maintenance_lines)/total_lines*100 if total_lines>0 else 0
        operational_lines=reliability_lines[reliability_lines["Status"].astype(str).str.lower().str.contains("operat")]
        operational_percentage=len(operational_lines)/total_lines*100 if total_lines>0 else 0

        metric1,metric2,metric3,metric4=st.columns(4)

        with metric1:
            st.metric("Total Grid Capacity",f"{total_capacity:,.0f} MVA")

        with metric2:
            st.metric("Total Substations",f"{total_substations:,}")

        with metric3:
            st.metric("Transmission Lines",f"{total_lines:,}")

        with metric4:
            st.metric("Lines Under Maintenance",f"{len(maintenance_lines):,}",f"{maintenance_percentage:.1f}%")

        st.divider()

        st.subheader("Infrastructure Reliability Status")
        status_counts=reliability_lines["Status"].fillna("Unknown").value_counts().reset_index()
        status_counts.columns=["Status","Count"]
        status_col1,status_col2=st.columns(2)

        with status_col1:
            status_figure=px.pie(status_counts,names="Status",values="Count",title="Transmission Line Status Distribution",hole=0.45)
            st.plotly_chart(status_figure,use_container_width=True)

        with status_col2:
            status_bar=px.bar(status_counts,x="Status",y="Count",title="Infrastructure Status",labels={"Status":"Status","Count":"Number of Lines"})
            st.plotly_chart(status_bar,use_container_width=True)

        st.divider()

        st.subheader("Capacity Analysis by Region")
        regional_capacity=reliability_substations.groupby("Region",dropna=False)["Capacity (MVA)"].sum().reset_index().sort_values("Capacity (MVA)",ascending=False)
        regional_capacity_figure=px.bar(regional_capacity,x="Region",y="Capacity (MVA)",title="Total Substation Capacity by Region",labels={"Region":"Region","Capacity (MVA)":"Total Capacity (MVA)"})
        regional_capacity_figure.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(regional_capacity_figure,use_container_width=True)

        st.divider()

        st.subheader("Capacity by Voltage Level")
        voltage_capacity=reliability_substations.groupby("Voltage (kV)",dropna=False)["Capacity (MVA)"].sum().reset_index().sort_values("Voltage (kV)")
        voltage_figure=px.bar(voltage_capacity,x="Voltage (kV)",y="Capacity (MVA)",title="Grid Capacity by Voltage Level",labels={"Voltage (kV)":"Voltage Level (kV)","Capacity (MVA)":"Total Capacity (MVA)"})
        st.plotly_chart(voltage_figure,use_container_width=True)

        st.divider()

        st.subheader("Utility Infrastructure Performance")
        utility_line_information=reliability_lines.groupby("Utility ID",dropna=False).agg(Transmission_Lines=("Line ID","count"),Total_Line_Capacity=("Capacity (MVA)","sum"),Total_Line_Length=("Length (km)","sum")).reset_index()
        utility_performance=utility_line_information.merge(reliability_utilities[["Utility ID","Name"]],on="Utility ID",how="left")
        utility_performance["Name"]=utility_performance["Name"].fillna("Unknown")
        utility_figure=px.bar(utility_performance,x="Name",y="Total_Line_Capacity",title="Transmission Capacity by Utility",labels={"Name":"Utility","Total_Line_Capacity":"Line Capacity (MVA)"})
        utility_figure.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(utility_figure,use_container_width=True)

        st.divider()

        st.subheader("Utility Infrastructure Comparison")
        utility_scatter=px.scatter(utility_performance,x="Transmission_Lines",y="Total_Line_Capacity",size="Total_Line_Length",hover_name="Name",title="Utility Transmission Infrastructure",labels={"Transmission_Lines":"Number of Transmission Lines","Total_Line_Capacity":"Total Line Capacity (MVA)","Total_Line_Length":"Total Line Length (km)"})
        st.plotly_chart(utility_scatter,use_container_width=True)

        st.divider()

        st.subheader("Highest-Capacity Substations")
        top_substations=reliability_substations[["Substation ID","Name","Region","Voltage (kV)","Capacity (MVA)","Status"]].sort_values("Capacity (MVA)",ascending=False).head(10)
        st.dataframe(top_substations,use_container_width=True,hide_index=True)

        st.divider()

        st.subheader("Capacity Concentration Analysis")
        total_national_capacity=reliability_substations["Capacity (MVA)"].sum()
        number_of_top_substations=max(1,int(len(reliability_substations)*0.10))
        top_10_capacity=reliability_substations["Capacity (MVA)"].nlargest(number_of_top_substations).sum()
        capacity_concentration=top_10_capacity/total_national_capacity*100 if total_national_capacity>0 else 0
        concentration_column1,concentration_column2=st.columns(2)

        with concentration_column1:
            st.metric("Top 10% Capacity Concentration",f"{capacity_concentration:.2f}%")

        with concentration_column2:
            st.metric("Operational Line Percentage",f"{operational_percentage:.2f}%")

        st.write("The capacity concentration measures the percentage of total substation capacity provided by the largest 10% of substations. A high value indicates that a small number of substations are responsible for majority of the grid's capacity.")

   

with tab5:
    st.title("Search Tab")
    st.write("Search for specific substations and lines!")
    st.write("Search & Compare")
    st.subheader("Substation Search")

    search_substation=st.text_input("Enter substation name or ID")

    if search_substation:
        substation_results=substations[substations["Name"].astype(str).str.contains(search_substation,case=False,na=False)|substations["Substation ID"].astype(str).str.contains(search_substation,case=False,na=False)]
        st.write("Substations found:",len(substation_results))
        st.dataframe(substation_results,use_container_width=True,hide_index=True)

    st.divider()

    st.subheader("Transmission Line Search")
    search_line=st.text_input("Enter line ID or substation name")

    if search_line:
        line_results=lines[lines["Line ID"].astype(str).str.contains(search_line,case=False,na=False)|lines["Source Substation"].astype(str).str.contains(search_line,case=False,na=False)|lines["Destination Substation"].astype(str).str.contains(search_line,case=False,na=False)]
        st.write("Transmission lines found:",len(line_results))
        st.dataframe(line_results,use_container_width=True,hide_index=True)

    st.divider()

    st.subheader("Utility Comparison")
    utility_names=utilities["Name"].dropna().unique().tolist()
    selected_utilities=st.multiselect("Select utilities to compare",utility_names)

    if selected_utilities:
        selected_utilities_data=utilities[utilities["Name"].isin(selected_utilities)]
        utility_ids=selected_utilities_data["Utility ID"].tolist()
        utility_lines=lines[lines["Utility ID"].isin(utility_ids)]
        utility_comparison=utility_lines.groupby("Utility ID").agg(Transmission_Lines=("Line ID","count"),Total_Capacity=("Capacity (MVA)","sum"),Total_Length=("Length (km)","sum")).reset_index()
        utility_comparison=utility_comparison.merge(utilities[["Utility ID","Name"]],on="Utility ID",how="left")
        utility_comparison=utility_comparison[["Name","Transmission_Lines","Total_Capacity","Total_Length"]]
        utility_comparison.columns=["Utility","Transmission Lines","Total Capacity (MVA)","Total Length (km)"]
        st.dataframe(utility_comparison,use_container_width=True,hide_index=True)
        utility_chart=px.bar(utility_comparison,x="Utility",y="Total Capacity (MVA)",title="Utility Capacity Comparison")
        st.plotly_chart(utility_chart,use_container_width=True)

  



# run command: python -m streamlit run "National Electricity Grid Network Analysis/Task 3/Task 3.1.py"