import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import json

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="EV Cell Management System",
    page_icon="🔋",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
if "cells_data" not in st.session_state:
    st.session_state.cells_data = pd.DataFrame({
        "Cell": [f"Cell {i}" for i in range(1, 5)],
        "Capacity (%)": np.random.randint(70, 100, 4),
        "Temperature (°C)": np.random.randint(25, 50, 4),
        "Efficiency (%)": np.random.randint(75, 98, 4),
    })

# ---------------- HEALTH CALCULATION ----------------
def calculate_health(capacity):
    if capacity > 85:
        return "Good"
    elif capacity > 75:
        return "Average"
    else:
        return "Poor"

st.session_state.cells_data["Health Status"] = st.session_state.cells_data["Capacity (%)"].apply(calculate_health)

# ---------------- TITLE ----------------
st.title("🔋 EV Battery Cell Management Dashboard")
st.markdown("Add, remove and monitor **EV battery cells** dynamically.")

st.divider()

# ---------------- ADD CELLS ----------------
st.sidebar.header("➕ Add Cells")

num_new_cells = st.sidebar.number_input(
    "Number of cells to add",
    min_value=1,
    max_value=20,
    value=1
)

if st.sidebar.button("Add Cell(s)"):
    current_count = len(st.session_state.cells_data)
    new_cells = []

    for i in range(num_new_cells):
        new_cells.append({
            "Cell": f"Cell {current_count + i + 1}",
            "Capacity (%)": np.random.randint(70, 100),
            "Temperature (°C)": np.random.randint(25, 50),
            "Efficiency (%)": np.random.randint(75, 98),
        })

    new_df = pd.DataFrame(new_cells)
    st.session_state.cells_data = pd.concat(
        [st.session_state.cells_data, new_df],
        ignore_index=True
    )
    st.success(f"{num_new_cells} cell(s) added successfully!")

# ---------------- REMOVE CELL ----------------
st.sidebar.header("➖ Remove Cell")

cell_to_remove = st.sidebar.selectbox(
    "Select cell to remove",
    st.session_state.cells_data["Cell"]
)

if st.sidebar.button("Remove Selected Cell"):
    st.session_state.cells_data = st.session_state.cells_data[
        st.session_state.cells_data["Cell"] != cell_to_remove
    ]
    st.success(f"{cell_to_remove} removed!")

df = st.session_state.cells_data

st.divider()

# ---------------- INTERACTIVE CHARTS ----------------
st.header("📊 Interactive Charts")

col1, col2 = st.columns(2)

with col1:
    fig1 = px.bar(
        df,
        x="Cell",
        y="Capacity (%)",
        color="Capacity (%)",
        title="Capacity Analysis",
        color_continuous_scale="Greens"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.line(
        df,
        x="Cell",
        y="Temperature (°C)",
        markers=True,
        title="Temperature Profile"
    )
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    fig3 = px.pie(
        df,
        names="Cell",
        values="Efficiency (%)",
        title="Efficiency Distribution"
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4 = px.histogram(
        df,
        x="Health Status",
        color="Health Status",
        title="Health Status Overview"
    )
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ---------------- BATTERY VISUALIZATION ----------------
st.header("🟢 Battery Visualization")

for _, row in df.iterrows():
    icon = "🟢" if row["Health Status"] == "Good" else "🟡" if row["Health Status"] == "Average" else "🔴"
    st.markdown(
        f"""
        **{row['Cell']}**  
        {icon} Capacity: **{row['Capacity (%)']}%** | 
        🌡️ Temp: **{row['Temperature (°C)']}°C** | 
        ⚡ Efficiency: **{row['Efficiency (%)']}%**
        """
    )

st.divider()

# ---------------- DATA TABLE ----------------
st.header("📋 Performance Metrics")
st.dataframe(df, use_container_width=True)

st.divider()

# ---------------- EXPORT OPTIONS ----------------
st.header("📦 Export Options")

col5, col6 = st.columns(2)

with col5:
    st.download_button(
        "⬇️ Download CSV",
        df.to_csv(index=False),
        "ev_cell_data.csv",
        "text/csv"
    )

with col6:
    st.download_button(
        "⬇️ Download JSON",
        json.dumps(df.to_dict(orient="records"), indent=4),
        "ev_cell_data.json",
        "application/json"
    )

# ---------------- FOOTER ----------------
st.markdown("🔧 **EV Cell Management System** | Dynamic Add & Remove Cells")
