import streamlit as st
import folium
import streamlit_folium as sf
import pandas as pd
from geopy.distance import geodesic
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import networkx as nx
import math
from folium.plugins import HeatMap


# Set page configuration
st.set_page_config(
    page_title="National Electricity Grid Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("⚡ National Electricity Grid Network Analysis")
st.caption("Task 3.2 Visualization Showcase")

# Data loading and processing
@st.cache_data
def load_and_prepare_data():
    utilities = pd.read_csv('grid-analysis/data_files/utilities.csv') # utilities.csv
    substations = pd.read_csv('grid-analysis/data_files/substations.csv') # substations.csv
    lines = pd.read_csv('grid-analysis/data_files/lines.csv') # lines.csv


    substation_coordinates = (
        substations.set_index("Substation ID")[["Latitude", "Longitude"]]
        .apply(tuple, axis=1)
        .to_dict()
    )

    def calculate_geodesic_distance(line):
        source_id = line["Source Substation ID"]
        destination_id = line["Destination Substation ID"]
        if source_id not in substation_coordinates or destination_id not in substation_coordinates:
            return np.nan
        return geodesic(substation_coordinates[source_id], substation_coordinates[destination_id]).km

    lines["Geodesic Distance (km)"] = lines.apply(calculate_geodesic_distance, axis=1)
    lines["Distance Difference (km)"] = lines["Length (km)"] - lines["Geodesic Distance (km)"]

    lines_with_utility = lines.merge(
        utilities[["Utility ID", "Name"]].rename(columns={"Name": "Utility Name"}),
        on="Utility ID",
        how="left"
    )

    lines_with_geographic_data = lines_with_utility.merge(
        substations[["Substation ID", "Latitude", "Longitude"]].rename(
            columns={"Latitude": "Source Latitude", "Longitude": "Source Longitude"}
        ),
        left_on="Source Substation ID", right_on="Substation ID", how="left"
    ).drop(columns="Substation ID")

    lines_with_geographic_data = lines_with_geographic_data.merge(
        substations[["Substation ID", "Latitude", "Longitude"]].rename(
            columns={"Latitude": "Destination Latitude", "Longitude": "Destination Longitude"}
        ),
        left_on="Destination Substation ID", right_on="Substation ID", how="left"
    ).drop(columns="Substation ID")

    substation_region_lookup = substations.set_index("Substation ID")["Region"].to_dict()
    substation_country_lookup = substations.set_index("Substation ID")["Country"].to_dict()

    lines_with_geographic_data["Source Region"] = lines_with_geographic_data["Source Substation ID"].map(substation_region_lookup)
    lines_with_geographic_data["Destination Region"] = lines_with_geographic_data["Destination Substation ID"].map(substation_region_lookup)
    lines_with_geographic_data["Source Country"] = lines_with_geographic_data["Source Substation ID"].map(substation_country_lookup)
    lines_with_geographic_data["Destination Country"] = lines_with_geographic_data["Destination Substation ID"].map(substation_country_lookup)

    def classify_connectivity(row):
        if row["Source Country"] != row["Destination Country"]:
            return "Cross-border"
        elif row["Source Region"] != row["Destination Region"]:
            return "Inter-regional"
        else:
            return "Intra-regional"

    lines_with_geographic_data["Connectivity Type"] = lines_with_geographic_data.apply(classify_connectivity, axis=1)

    connected_line_counts = {}
    for _, line in lines.iterrows():
        source = line["Source Substation ID"]
        destination = line["Destination Substation ID"]
        connected_line_counts[source] = connected_line_counts.get(source, 0) + 1
        connected_line_counts[destination] = connected_line_counts.get(destination, 0) + 1

    substations["Connected Lines"] = substations["Substation ID"].map(connected_line_counts).fillna(0)

    return utilities, substations, lines, lines_with_geographic_data

utilities, substations, lines, lines_with_geographic_data = load_and_prepare_data()

# Sidebar metrics
st.sidebar.header("Grid Summary")
st.sidebar.metric("Utilities", len(utilities))
st.sidebar.metric("Substations", len(substations))
st.sidebar.metric("Transmission Lines", len(lines))


# Navigation tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🕸️ Networks & 3D",
    "🔄 Flows & Chord",
    "🗺️ Heatmaps",
    "📈 Utility Footprint",
    "🏭 Substations",
    "⏳ Grid Expansion"
])


with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Interactive Force-Directed Graph")
        G = nx.Graph()
        for _, sub in substations.iterrows():
            G.add_node(sub["Substation ID"], name=sub["Name"], region=sub["Region"], country=sub["Country"],
                       voltage=sub["Voltage (kV)"], capacity=sub["Capacity (MVA)"], status=sub["Status"])

        for _, line in lines.iterrows():
            if line["Source Substation ID"] in G.nodes and line["Destination Substation ID"] in G.nodes:
                G.add_edge(line["Source Substation ID"], line["Destination Substation ID"])

        positions = nx.spring_layout(G, seed=42, k=0.5, iterations=100)
        edge_x, edge_y = [], []
        for src, dst in G.edges():
            x0, y0 = positions[src]
            x1, y1 = positions[dst]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        edge_trace = go.Scatter(x=edge_x, y=edge_y, mode="lines", line=dict(width=1, color="#888"), hoverinfo="none")

        node_x, node_y, node_text, node_size = [], [], [], []
        for node in G.nodes():
            x, y = positions[node]
            node_x.append(x)
            node_y.append(y)
            info = G.nodes[node]
            node_text.append(f"<b>{info['name']}</b><br>Region: {info['region']}<br>Capacity: {info['capacity']} MVA")
            node_size.append(max(8, math.sqrt(max(info["capacity"], 1)) / 2))

        node_trace = go.Scatter(x=node_x, y=node_y, mode="markers", text=node_text, hoverinfo="text", marker=dict(size=node_size, color="#1f77b4"))

        fig_net = go.Figure(data=[edge_trace, node_trace])
        fig_net.update_layout(showlegend=False, xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                              yaxis=dict(showgrid=False, zeroline=False, showticklabels=False), margin=dict(l=0, r=0, b=0, t=30))
        st.plotly_chart(fig_net, use_container_width=True)

    with col2:
        st.subheader("3D Geographic Grid")
        coordinate_lookup = substations.set_index("Substation ID")[["Latitude", "Longitude"]].to_dict("index")
        fig_3d = go.Figure()

        for _, line in lines.iterrows():
            src, dst = line["Source Substation ID"], line["Destination Substation ID"]
            if src in coordinate_lookup and dst in coordinate_lookup:
                src_data, dst_data = coordinate_lookup[src], coordinate_lookup[dst]
                src_sub = substations[substations["Substation ID"] == src].iloc[0]
                dst_sub = substations[substations["Substation ID"] == dst].iloc[0]

                fig_3d.add_trace(go.Scatter3d(
                    x=[src_data["Longitude"], dst_data["Longitude"]],
                    y=[src_data["Latitude"], dst_data["Latitude"]],
                    z=[src_sub["Capacity (MVA)"], dst_sub["Capacity (MVA)"]],
                    mode="lines", line=dict(width=3, color="#666"), showlegend=False, hoverinfo="none"
                ))

        sub_text = [f"<b>{row['Name']}</b><br>Capacity: {row['Capacity (MVA)']} MVA" for _, row in substations.iterrows()]
        fig_3d.add_trace(go.Scatter3d(
            x=substations["Longitude"], y=substations["Latitude"], z=substations["Capacity (MVA)"],
            mode="markers", text=sub_text, hoverinfo="text", marker=dict(size=5, color="#d62728")
        ))
        fig_3d.update_layout(scene=dict(xaxis_title="Longitude", yaxis_title="Latitude", zaxis_title="Capacity (MVA)"), margin=dict(l=0, r=0, b=0, t=30))
        st.plotly_chart(fig_3d, use_container_width=True)


with tab2:
    st.subheader("Inter-Regional Transmission Flow Diagram")
    regional_flows = lines_with_geographic_data.dropna(subset=["Source Region", "Destination Region"]).groupby(["Source Region", "Destination Region"]).size().reset_index(name="Line Count")
    regional_flows = regional_flows[regional_flows["Source Region"] != regional_flows["Destination Region"]]

    regions = sorted(set(regional_flows["Source Region"]) | set(regional_flows["Destination Region"]))

    if len(regions) > 0:
        region_totals = {region: 0 for region in regions}
        for _, row in regional_flows.iterrows():
            region_totals[row["Source Region"]] += row["Line Count"]
            region_totals[row["Destination Region"]] += row["Line Count"]

        total_flow = sum(region_totals.values())
        gap = 0.04
        available_angle = (2 * np.pi - gap * len(regions))
        region_angles = {}
        current_angle = 0

        for region in regions:
            size = (region_totals[region] / total_flow * available_angle)
            region_angles[region] = (current_angle, current_angle + size)
            current_angle += (size + gap)

        chord_fig = go.Figure()
        for region in regions:
            start_angle, end_angle = region_angles[region]
            angles = np.linspace(start_angle, end_angle, 60)
            chord_fig.add_trace(go.Scatter(x=np.cos(angles), y=np.sin(angles), mode="lines", line=dict(width=12), name=region))

        region_used_angle = {region: region_angles[region][0] for region in regions}
        for _, row in regional_flows.iterrows():
            src, tgt, flow = row["Source Region"], row["Destination Region"], row["Line Count"]
            src_start, src_end = region_angles[src]
            tgt_start, tgt_end = region_angles[tgt]

            src_a1 = region_used_angle[src]
            src_a2 = src_a1 + ((src_end - src_start) * flow / region_totals[src])
            region_used_angle[src] = src_a2

            tgt_a1 = region_used_angle[tgt]
            tgt_a2 = tgt_a1 + ((tgt_end - tgt_start) * flow / region_totals[tgt])
            region_used_angle[tgt] = tgt_a2

            src_angles = np.linspace(src_a1, src_a2, 20)
            tgt_angles = np.linspace(tgt_a1, tgt_a2, 20)
            src_points = [(np.cos(a) * 0.94, np.sin(a) * 0.94) for a in src_angles]
            tgt_points = [(np.cos(a) * 0.94, np.sin(a) * 0.94) for a in tgt_angles]

            ribbon_x = [p[0] for p in src_points] + [p[0] for p in reversed(tgt_points)]
            ribbon_y = [p[1] for p in src_points] + [p[1] for p in reversed(tgt_points)]

            chord_fig.add_trace(go.Scatter(x=ribbon_x, y=ribbon_y, mode="lines", fill="toself", line=dict(width=0), opacity=0.45, showlegend=False))

        for region in regions:
            start, end = region_angles[region]
            mid = (start + end) / 2
            chord_fig.add_annotation(x=np.cos(mid) * 1.12, y=np.sin(mid) * 1.12, text=region, showarrow=False)

        chord_fig.update_layout(xaxis=dict(visible=False, range=[-1.3, 1.3]), yaxis=dict(visible=False, range=[-1.3, 1.3], scaleanchor="x"), margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(chord_fig, use_container_width=True)


with tab3:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Geographic Line Density Heatmap")
        map_center = [substations["Latitude"].mean(), substations["Longitude"].mean()]
        heatmap_data = [[s["Latitude"], s["Longitude"], s["Connected Lines"]] for _, s in substations.iterrows()]
        line_density_map = folium.Map(location=map_center, zoom_start=6)
        HeatMap(heatmap_data, radius=25, blur=20, min_opacity=0.4).add_to(line_density_map)

        sf.folium_static(line_density_map, height=450, width=None)

    with col2:
        st.subheader("Maintenance Status Concentration")
        maint_summary = lines_with_geographic_data.dropna(subset=["Source Region", "Status"]).groupby(["Source Region", "Status"]).size().reset_index(name="Line Count")
        maint_matrix = maint_summary.pivot(index="Source Region", columns="Status", values="Line Count").fillna(0)
        fig_maint = px.imshow(maint_matrix, text_auto=True, aspect="auto", labels=dict(x="Status", y="Region", color="Lines"))
        st.plotly_chart(fig_maint, use_container_width=True)



with tab4:
    st.subheader("Utility Infrastructure Metrics")
    utility_metrics = lines_with_geographic_data.groupby("Utility Name").agg(
        Transmission_Lines=("Line ID", "count"),
        Total_Line_Length_km=("Length (km)", "sum"),
        Total_Capacity_MVA=("Capacity (MVA)", "sum")
    ).reset_index()

    metric_choice = st.radio("Select Metric to Display:", ["Transmission Lines", "Total Line Length (km)", "Total Capacity (MVA)"], horizontal=True)

    col_map = {
        "Transmission Lines": "Transmission_Lines",
        "Total Line Length (km)": "Total_Line_Length_km",
        "Total Capacity (MVA)": "Total_Capacity_MVA"
    }

    fig_util = px.bar(utility_metrics, x="Utility Name", y=col_map[metric_choice], color="Utility Name", title=f"{metric_choice} by Utility")
    st.plotly_chart(fig_util, use_container_width=True)



with tab5:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 15 Substations by Capacity")
        top_substations = substations.sort_values("Capacity (MVA)", ascending=False).head(15)
        fig_cap = px.bar(top_substations, x="Name", y="Capacity (MVA)", color="Region")
        fig_cap.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_cap, use_container_width=True)

    with col2:
        st.subheader("Total Capacity by Region")
        reg_metrics = substations.groupby("Region").agg(Total_Capacity_MVA=("Capacity (MVA)", "sum")).reset_index()
        fig_reg = px.bar(reg_metrics, x="Region", y="Total_Capacity_MVA", color="Region")
        fig_reg.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_reg, use_container_width=True)



with tab6:
    st.subheader("Grid Expansion Over Time")

    anim_subs = substations.copy()
    anim_subs["Commissioning Year"] = pd.to_numeric(anim_subs["Commissioning Year"], errors="coerce")
    anim_subs = anim_subs.dropna(subset=["Commissioning Year", "Latitude", "Longitude"])
    anim_subs["Commissioning Year"] = anim_subs["Commissioning Year"].astype(int)

    years = sorted(anim_subs["Commissioning Year"].unique())
    selected_year = st.select_slider("Filter/Play by Year:", options=years, value=years[-1])

    active_subs = anim_subs[anim_subs["Commissioning Year"] <= selected_year]

    fig_exp = px.scatter_mapbox(
        active_subs, lat="Latitude", lon="Longitude", size="Capacity (MVA)",
        hover_name="Name", hover_data=["Region", "Commissioning Year"],
        zoom=5, mapbox_style="open-street-map",
        title=f"Substations Active up to {selected_year}"
    )
    fig_exp.update_layout(margin=dict(l=0, r=0, b=0, t=30))
    st.plotly_chart(fig_exp, use_container_width=True)
