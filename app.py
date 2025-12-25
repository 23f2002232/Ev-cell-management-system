import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="EV Cell Management System",
    page_icon="🔋",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
if "cells" not in st.session_state:
    st.session_state.cells = pd.DataFrame(columns=[
        "Cell ID",
        "Cell Type",
        "Voltage (V)",
        "Current (A)",
        "Capacity (%)",
        "Cooling Temp (°C)",
        "Efficiency (%)",
        "Health Status"
    ])

# ---------------- FUNCTIONS ----------------
def calculate_health(capacity, temp):
    if capacity > 85 and temp < 45:
        return "Good"
    elif capacity > 70:
        return "Average"
    else:
        return "Poor"

# ---------------- TITLE ----------------
st.title("EV Battery Cell Management Dashboard")
st.markdown(
    "Monitor and manage **electric vehicle battery cells** using real-time performance indicators."
)

st.divider()

# ================= ADD CELL FORM =================
st.header("➕ Add New Battery Cell")

with st.form("add_cell_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        cell_id = st.text_input("Cell ID", placeholder="e.g. Cell 01")
        cell_type = st.selectbox("Cell Type", ["Lithium-ion", "LFP", "NMC", "Solid State"])

    with col2:
        voltage = st.number_input("Voltage (V)", min_value=0.0, step=0.1)
        current = st.number_input("Current (A)", min_value=0.0, step=0.1)

    with col3:
        capacity = st.slider("Capacity (%)", 0, 100, 80)
        cooling_temp = st.number_input("Cooling Temperature (°C)", min_value=0.0, step=0.5)

    submit = st.form_submit_button("Add Cell")

    if submit:
        efficiency = round((voltage * current) / 10, 2) if voltage > 0 else 0
        health = calculate_health(capacity, cooling_temp)

        new_cell = pd.DataFrame([{
            "Cell ID": cell_id,
            "Cell Type": cell_type,
            "Voltage (V)": voltage,
            "Current (A)": current,
            "Capacity (%)": capacity,
            "Cooling Temp (°C)": cooling_temp,
            "Efficiency (%)": efficiency,
            "Health Status": health
        }])

        st.session_state.cells = pd.concat(
            [st.session_state.cells, new_cell],
            ignore_index=True
        )

        st.success("Battery cell added successfully")

st.divider()


# ================= REMOVE CELL =================
st.header("➖ Remove Battery Cell")

if not st.session_state.cells.empty:
    col_r1, col_r2 = st.columns([3, 1])

    with col_r1:
        remove_cell_id = st.selectbox(
            "Select Cell ID to Remove",
            st.session_state.cells["Cell ID"]
        )

    with col_r2:
        if st.button("Remove Cell"):
            st.session_state.cells = st.session_state.cells[
                st.session_state.cells["Cell ID"] != remove_cell_id
            ]
            st.success(f"{remove_cell_id} removed successfully")
else:
    st.info("No cells available to remove.")


# ================= DATA TABLE =================
st.header("📋 Cell Performance Data")
st.dataframe(st.session_state.cells, use_container_width=True)

st.divider()

# ================= PERFORMANCE GRAPHS =================
st.header("📊 Performance Analysis")

if not st.session_state.cells.empty:
    col4, col5 = st.columns(2)

    with col4:
        fig1 = px.bar(
            st.session_state.cells,
            x="Cell ID",
            y="Capacity (%)",
            color="Health Status",
            title="Cell Capacity Comparison"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col5:
        fig2 = px.scatter(
            st.session_state.cells,
            x="Voltage (V)",
            y="Current (A)",
            size="Efficiency (%)",
            color="Cell Type",
            title="Voltage vs Current Performance"
        )
        st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.line(
        st.session_state.cells,
        x="Cell ID",
        y="Cooling Temp (°C)",
        markers=True,
        title="Cooling Temperature Trend"
    )
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("No cells added yet. Please add a battery cell to see analysis.")

st.divider()

# ================= FOOTER =================
st.markdown(
    """
    **EV Cell Management System**  
    Designed for monitoring battery health, electrical performance, and thermal safety.
    """
)
