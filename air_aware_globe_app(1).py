import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# ============================================================
# AIR AWARE — INTERACTIVE AIR QUALITY GLOBE
# ============================================================

st.set_page_config(
    page_title="AirAware | Air Quality Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------- DESIGN ---------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #070B14;
    color: #E8EEF8;
}

header[data-testid="stHeader"] {
    background: rgba(7, 11, 20, 0.8);
}

.block-container {
    padding-top: 1.3rem;
    padding-bottom: 1rem;
    max-width: 1600px;
}

section[data-testid="stSidebar"] {
    background: #0B1220;
    border-right: 1px solid #202B3E;
}

section[data-testid="stSidebar"] * {
    color: #DCE5F5;
}

.brand {
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -1px;
    color: #F3F7FF;
}

.brand span {
    color: #43E6B0;
}

.sub-brand {
    color: #8393AB;
    font-size: 11px;
    letter-spacing: 2px;
    margin-top: 3px;
}

.section-label {
    color: #8191A9;
    font-size: 10px;
    letter-spacing: 2px;
    font-weight: 700;
    margin: 20px 0 8px 0;
}

.metric-card {
    background: linear-gradient(135deg, #111B2D, #0C1423);
    border: 1px solid #233149;
    border-radius: 13px;
    padding: 17px 18px;
    min-height: 115px;
}

.metric-label {
    font-size: 11px;
    color: #91A0B7;
    margin-bottom: 10px;
}

.metric-value {
    font-size: 27px;
    font-weight: 800;
    color: #F3F7FF;
}

.metric-foot {
    font-size: 11px;
    color: #43E6B0;
    margin-top: 7px;
}

.panel {
    background: #0C1423;
    border: 1px solid #233149;
    border-radius: 13px;
    padding: 17px;
    margin-bottom: 12px;
}

.panel-title {
    color: #EDF3FF;
    font-weight: 700;
    font-size: 15px;
}

.muted {
    color: #8393AB;
    font-size: 12px;
}

.status-dot {
    display: inline-block;
    height: 8px;
    width: 8px;
    border-radius: 50%;
    background: #43E6B0;
    margin-right: 7px;
}

div[data-testid="stSelectbox"] label,
div[data-testid="stSlider"] label,
div[data-testid="stCheckbox"] label {
    color: #B6C3D7;
}

.stButton > button {
    border-radius: 9px;
    border: 1px solid #2D435C;
    background: #142238;
    color: #E8EEF8;
}

.stButton > button:hover {
    border-color: #43E6B0;
    color: #43E6B0;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #233149;
    border-radius: 10px;
}

hr {
    border-color: #202B3E;
}
</style>
""", unsafe_allow_html=True)


# --------------------- SAMPLE DATA -------------------------

# Demo locations and readings. Replace these with real
# monitoring station data when your data pipeline is ready.

@st.cache_data
def get_demo_data():
    return pd.DataFrame([
        ["Delhi - Anand Vihar", 28.6469, 77.3160, 186, 94, 72, 48],
        ["Delhi - RK Puram", 28.5633, 77.1869, 142, 81, 55, 36],
        ["Delhi - Dwarka", 28.5921, 77.0460, 118, 67, 42, 29],
        ["Delhi - Punjabi Bagh", 28.6740, 77.1310, 159, 85, 61, 41],
        ["Delhi - ITO", 28.6280, 77.2410, 171, 89, 67, 44],
        ["Noida - Sector 62", 28.6270, 77.3649, 136, 76, 48, 33],
        ["Gurugram - Sector 51", 28.4260, 77.0720, 109, 61, 37, 26],
        ["Chandigarh", 30.7333, 76.7794, 68, 37, 25, 18],
        ["Jaipur", 26.9124, 75.7873, 79, 44, 31, 21],
        ["Lucknow", 26.8467, 80.9462, 125, 71, 46, 31],
        ["Mumbai", 19.0760, 72.8777, 64, 36, 22, 17],
        ["Pune", 18.5204, 73.8567, 48, 28, 17, 12],
        ["Ahmedabad", 23.0225, 72.5714, 91, 52, 33, 24],
        ["Kolkata", 22.5726, 88.3639, 87, 49, 32, 23],
        ["Bengaluru", 12.9716, 77.5946, 35, 20, 13, 10],
        ["Hyderabad", 17.3850, 78.4867, 52, 30, 19, 14],
        ["Chennai", 13.0827, 80.2707, 43, 25, 16, 12],
        ["Bhopal", 23.2599, 77.4126, 76, 42, 29, 20],
        ["Patna", 25.5941, 85.1376, 132, 75, 49, 35],
        ["Dehradun", 30.3165, 78.0322, 56, 31, 19, 14],
    ], columns=[
        "Station", "Latitude", "Longitude",
        "PM2.5", "PM10", "NO2", "O3"
    ])


df = get_demo_data()


def get_aqi_status(value):
    if value <= 50:
        return "Good", "#43E6B0"
    elif value <= 100:
        return "Moderate", "#D9E65C"
    elif value <= 150:
        return "Unhealthy for sensitive groups", "#FFA657"
    elif value <= 200:
        return "Unhealthy", "#FF647C"
    elif value <= 300:
        return "Very unhealthy", "#C084FC"
    return "Hazardous", "#FF4D4D"


def make_globe(data, pollutant, show_stations, show_labels):
    values = data[pollutant].astype(float)
    colors = [get_aqi_status(v)[1] for v in values]

    fig = go.Figure()

    # Station markers on a 3D-style globe.
    # Marker color represents the selected pollutant's
    # concentration band, NOT an official AQI calculation.

    fig.add_trace(go.Scattergeo(
        lon=data["Longitude"],
        lat=data["Latitude"],
        mode="markers+text" if show_labels else "markers",
        text=data["Station"] if show_labels else None,
        textposition="top center",
        textfont=dict(size=9, color="#C7D5EA"),
        customdata=np.column_stack([
            data["Station"],
            data[pollutant],
            data["Latitude"],
            data["Longitude"]
        ]),
        marker=dict(
            size=np.clip(values / 7, 8, 23) if show_stations else 0,
            color=colors,
            opacity=0.95,
            line=dict(color="#E8F1FF", width=0.7)
        ),
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            + pollutant + ": %{customdata[1]} µg/m³<br>"
            "Latitude: %{customdata[2]:.4f}<br>"
            "Longitude: %{customdata[3]:.4f}"
            "<extra></extra>"
        ),
        name="Monitoring stations"
    ))

    fig.update_geos(
        projection_type="orthographic",
        projection_rotation=dict(lon=78, lat=23, roll=0),
        showland=True,
        landcolor="#172638",
        showocean=True,
        oceancolor="#071426",
        showlakes=True,
        lakecolor="#0B1C30",
        showcoastlines=True,
        coastlinecolor="#30475E",
        coastlinewidth=0.6,
        showcountries=True,
        countrycolor="#30475E",
        countrywidth=0.6,
        showframe=False,
        bgcolor="#090F1B",
        lataxis_showgrid=True,
        lonaxis_showgrid=True,
        lataxis_gridcolor="#1B3047",
        lonaxis_gridcolor="#1B3047",
        lataxis_gridwidth=0.5,
        lonaxis_gridwidth=0.5
    )

    fig.update_layout(
        height=545,
        margin=dict(l=0, r=0, t=5, b=0),
        paper_bgcolor="#090F1B",
        plot_bgcolor="#090F1B",
        font=dict(family="Inter", color="#DCE5F5"),
        showlegend=False
    )

    return fig


# ----------------------- SIDEBAR ---------------------------

with st.sidebar:
    st.markdown("""
    <div style="padding: 8px 0 18px 0;">
        <div class="brand">AIR<span>AWARE</span></div>
        <div class="sub-brand">ATMOSPHERIC INTELLIGENCE</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    page = st.radio(
        "NAVIGATION",
        ["🌍  Globe Explorer", "📊  Air Quality Data", "ℹ️  About AirAware"],
        label_visibility="visible"
    )

    st.markdown("---")
    st.markdown('<div class="section-label">POLLUTION SETTINGS</div>',
                unsafe_allow_html=True)

    pollutant = st.selectbox(
        "Select pollutant",
        ["PM2.5", "PM10", "NO2", "O3"]
    )

    st.markdown('<div class="section-label">MAP LAYERS</div>',
                unsafe_allow_html=True)

    show_stations = st.checkbox("Monitoring stations", value=True)
    show_labels = st.checkbox("Station labels", value=False)

    st.markdown('<div class="section-label">REGION</div>',
                unsafe_allow_html=True)

    region = st.selectbox(
        "Select region",
        ["All India", "Delhi NCR", "North India", "South India"],
        label_visibility="collapsed"
    )

    if st.button("↻  Reset filters", use_container_width=True):
        st.session_state["reset_region"] = True
        st.rerun()

    st.markdown("---")

    st.markdown("""
    <div class="muted">
        <span class="status-dot"></span>Demo system active<br><br>
        DATA MODE: SIMULATED<br>
        VERSION: 0.1.0
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("AirAware • Student Research Prototype")


# ----------------------- FILTER DATA -----------------------

if st.session_state.pop("reset_region", False):
    st.session_state["region"] = "All India"

if region == "Delhi NCR":
    view_df = df[df["Station"].str.contains(
        "Delhi|Noida|Gurugram", case=False, regex=True
    )].copy()
elif region == "North India":
    view_df = df[df["Station"].isin([
        "Delhi - Anand Vihar", "Delhi - RK Puram",
        "Delhi - Dwarka", "Delhi - Punjabi Bagh",
        "Delhi - ITO", "Noida - Sector 62",
        "Gurugram - Sector 51", "Chandigarh",
        "Jaipur", "Lucknow", "Dehradun", "Patna"
    ])].copy()
elif region == "South India":
    view_df = df[df["Station"].isin([
        "Bengaluru", "Hyderabad", "Chennai", "Pune"
    ])].copy()
else:
    view_df = df.copy()


# -------------------- HEADER AND METRICS -------------------

st.markdown("""
<div style="display:flex; justify-content:space-between;
align-items:center; flex-wrap:wrap; gap:10px;">
    <div>
        <div style="font-size:27px; font-weight:800;
        letter-spacing:-0.8px;">Air Quality Globe</div>
        <div style="color:#8798B1; font-size:12px; margin-top:5px;">
        Explore pollution patterns across monitoring locations in India
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")

col1, col2, col3, col4 = st.columns(4)

avg_value = view_df[pollutant].mean()
peak_value = view_df[pollutant].max()
worst_station = view_df.loc[view_df[pollutant].idxmax(), "Station"]
status, status_color = get_aqi_status(avg_value)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">AVERAGE {pollutant}</div>
        <div class="metric-value">{avg_value:.1f}</div>
        <div class="metric-foot">µg/m³ · Demo readings</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">MONITORING LOCATIONS</div>
        <div class="metric-value">{len(view_df)}</div>
        <div class="metric-foot">Locations in selected region</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">HIGHEST READING</div>
        <div class="metric-value">{peak_value:.0f}</div>
        <div class="metric-foot">µg/m³ · {worst_station}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">AVERAGE CONCENTRATION BAND</div>
        <div style="font-size:19px; font-weight:800; color:{status_color};
        margin-top:5px;">{status}</div>
        <div class="metric-foot" style="color:#91A0B7;">
        Indicative band, not official AQI
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ------------------------ MAIN PAGE ------------------------

if page == "🌍  Globe Explorer":

    left, right = st.columns([1.8, 1], gap="medium")

    with left:
        st.markdown("""
        <div class="panel-title">🌐 Interactive Earth</div>
        <div class="muted">
        Select a marker to inspect a monitoring location.
        </div>
        """, unsafe_allow_html=True)

        globe = make_globe(
            view_df, pollutant, show_stations, show_labels
        )

        st.plotly_chart(
            globe,
            use_container_width=True,
            config={
                "displayModeBar": True,
                "scrollZoom": True,
                "displaylogo": False
            }
        )

        st.markdown("""
        <div class="muted">
        <span style="color:#43E6B0;">●</span> Lower concentration
        &nbsp;&nbsp;
        <span style="color:#D9E65C;">●</span> Moderate
        &nbsp;&nbsp;
        <span style="color:#FFA657;">●</span> Elevated
        &nbsp;&nbsp;
        <span style="color:#FF647C;">●</span> High
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="panel-title">📍 Station Intelligence</div>
        <div class="muted">Inspect individual station readings</div>
        """, unsafe_allow_html=True)

        selected_station = st.selectbox(
            "Monitoring station",
            view_df["Station"].tolist()
        )

        station = view_df[
            view_df["Station"] == selected_station
        ].iloc[0]

        station_value = station[pollutant]
        station_status, station_color = get_aqi_status(station_value)

        st.markdown(f"""
        <div class="panel">
            <div class="muted">SELECTED LOCATION</div>
            <div style="font-size:19px;font-weight:800;
            margin-top:8px;">{station["Station"]}</div>
            <div style="color:#8798B1;font-size:11px;margin-top:5px;">
            {station["Latitude"]:.4f}° N &nbsp;·&nbsp;
            {station["Longitude"]:.4f}° E
            </div>
            <hr>
            <div class="muted">{pollutant} CONCENTRATION</div>
            <div style="font-size:37px;font-weight:800;
            margin:8px 0;color:{station_color};">
            {station_value:.0f}
            <span style="font-size:13px;color:#9AAAC0;">µg/m³</span>
            </div>
            <div style="display:inline-block;padding:6px 10px;
            border:1px solid {station_color};border-radius:7px;
            color:{station_color};font-size:12px;">
            {station_status} concentration band
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**All pollutant readings**")

        pollutant_cols = st.columns(2)
        for i, p in enumerate(["PM2.5", "PM10", "NO2", "O3"]):
            with pollutant_cols[i % 2]:
                st.metric(p, f'{station[p]:.0f} µg/m³')

        st.markdown("""
        <div class="panel">
            <div class="panel-title">About this reading</div>
            <div class="muted" style="margin-top:10px;line-height:1.8;">
            Values currently come from a simulated dataset.
            They demonstrate the interface and are not live
            measurements from the displayed locations.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📈 Regional concentration comparison")

    chart_df = view_df.sort_values(pollutant, ascending=True)

    bar_fig = go.Figure(go.Bar(
        x=chart_df[pollutant],
        y=chart_df["Station"],
        orientation="h",
        marker=dict(
            color=[get_aqi_status(v)[1] for v in chart_df[pollutant]],
            line=dict(width=0)
        ),
        hovertemplate="%{y}<br>" + pollutant + ": %{x} µg/m³<extra></extra>"
    ))

    bar_fig.update_layout(
        height=max(300, len(chart_df) * 28),
        margin=dict(l=0, r=15, t=10, b=10),
        paper_bgcolor="#070B14",
        plot_bgcolor="#070B14",
        font=dict(color="#DCE5F5", size=11),
        xaxis=dict(
            title="Concentration (µg/m³)",
            gridcolor="#202B3E",
            zeroline=False
        ),
        yaxis=dict(
            title="",
            gridcolor="#202B3E"
        )
    )

    st.plotly_chart(bar_fig, use_container_width=True)


elif page == "📊  Air Quality Data":

    st.markdown("### Monitoring station dataset")
    st.markdown(
        "Review readings, compare locations, and export the demo dataset."
    )

    st.dataframe(
        view_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Latitude": st.column_config.NumberColumn(format="%.4f"),
            "Longitude": st.column_config.NumberColumn(format="%.4f"),
            "PM2.5": st.column_config.NumberColumn(format="%.1f µg/m³"),
            "PM10": st.column_config.NumberColumn(format="%.1f µg/m³"),
            "NO2": st.column_config.NumberColumn(format="%.1f µg/m³"),
            "O3": st.column_config.NumberColumn(format="%.1f µg/m³")
        }
    )

    csv = view_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download station data (CSV)",
        data=csv,
        file_name="airaware_station_data.csv",
        mime="text/csv"
    )

    st.info(
        "This is demonstration data. Replace it with verified monitoring "
        "station observations before using it for research conclusions."
    )


elif page == "ℹ️  About AirAware":

    st.markdown("### About AirAware")

    st.write("""
    AirAware is a student research prototype for exploring
    air pollution patterns across locations.

    The planned system can combine monitoring-station data,
    data cleaning, spatial interpolation, and machine-learning
    methods to estimate pollution at locations without sensors.
    """)

    st.markdown("#### Planned system architecture")

    st.code("""
Monitoring Stations / Open Datasets
                |
                v
       Data Collection Layer
                |
                v
        Data Cleaning
                |
                v
     Spatial Interpolation (IDW)
                |
                v
       Pollution Estimation
                |
                v
      Interactive Globe UI
    """, language="text")

    st.markdown("#### Technology stack")
    st.write(
        "- Python for data processing\n"
        "- Streamlit for the dashboard\n"
        "- Plotly for interactive globe visualization\n"
        "- Pandas and NumPy for data handling\n"
        "- IDW and machine learning for future spatial estimation"
    )

    st.warning(
        "The current version is a UI prototype. It does not yet "
        "fetch live data or calculate an IDW/ML pollution surface."
    )


# ------------------------ FOOTER ----------------------------

st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#65758D;font-size:11px;padding:5px;">
AirAware · Hyperlocal Air Quality Intelligence · Research Prototype
</div>
""", unsafe_allow_html=True)