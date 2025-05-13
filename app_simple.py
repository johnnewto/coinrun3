import streamlit as st
import pandas as pd
import numpy as np
import time

# Create initial empty DataFrame
index = 0.1
chart_data = pd.DataFrame({
    "GDP": np.random.randn(1),
    "years": np.random.randn(1),
}, index=[index])  # Add index


# st.line_chart(chart_data, x="col1", y="col2", x_label="Years", y_label="GDP")
# Create the chart container

chart = st.line_chart(chart_data, x_label="Years", y_label="GDP")

# Simulate real-time data updates
for i in range(20):
    index += 0.1
    # Create new data point
    new_data = pd.DataFrame({
        "GDP": [i],
        "years": [np.random.randn()],
    }, index=[index])  # Continue index from where initial data left off
    
    # Add the new row to the chart
    chart.add_rows(new_data)
    
    # Small delay to make the updates visible
    time.sleep(0.5)