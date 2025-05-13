import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# Set page config
st.set_page_config(page_title="Real-Time Line Chart", page_icon="📈", layout="wide")

# Dashboard title
st.title("Real-Time Line Chart")

# Initialize session state
if "points" not in st.session_state:
    st.session_state.points = {"x": [], "y": []}  # Store x, y coordinates
    st.session_state.fig = go.Figure(
        data=[go.Scatter(
            x=[], 
            y=[], 
            mode="lines+markers",  # Changed from "markers" to "lines+markers"
            marker=dict(size=8, color="blue"),
            line=dict(width=2, color="blue")  # Added line configuration
        )]
    )
    st.session_state.fig.update_layout(
        title="Real-Time Data Simulation",
        xaxis_title="Time",
        yaxis_title="Value",
        xaxis_range=[0, 20],  # Adjusted for time steps
        yaxis_range=[0, 10],
        showlegend=False,
    )
    st.session_state.count = 0

# Create chart container
chart_placeholder = st.empty()

# Render initial chart
with chart_placeholder:
    st.plotly_chart(st.session_state.fig, use_container_width=True, key=f"line_realtime_{st.session_state.count}")

# Real-time simulation
for _ in range(20):
    # Generate new point
    new_x = st.session_state.count  # Use count as x-axis (time)
    new_y = np.random.uniform(0, 10)

    # Append new point
    st.session_state.points["x"].append(new_x)
    st.session_state.points["y"].append(new_y)

    # Keep only the last 100 points
    if len(st.session_state.points["x"]) > 100:
        st.session_state.points["x"] = st.session_state.points["x"][-100:]
        st.session_state.points["y"] = st.session_state.points["y"][-100:]

    # Update scatter trace
    st.session_state.fig.data[0].x = st.session_state.points["x"]
    st.session_state.fig.data[0].y = st.session_state.points["y"]

    # Increment counter
    st.session_state.count += 1

    # Update chart with unique key
    with chart_placeholder:
        st.plotly_chart(st.session_state.fig, use_container_width=True, key=f"line_realtime_{st.session_state.count}")

    time.sleep(0.5)  # Update every 0.5 seconds
    print("Updated", st.session_state.count)