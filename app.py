import streamlit as st
# import numpy as np
import time
import pandas as pd

from pyminsky import minsky

# Set page config
st.set_page_config(page_title="Minsky GDP Simulation", page_icon="📈", layout="wide")

# Dashboard title
st.title("Minsky GDP Simulation")

# Add controls to sidebar
with st.sidebar:
    st.header("Simulation Controls")
    update_freq = st.slider("Update every N steps", min_value=1, max_value=50, value=10, step=1)
    total_steps = st.slider("Total simulation steps", min_value=100, max_value=10000, value=1000, step=100)

# Initialize session state
if "simulation_data" not in st.session_state:
    # Initialize lists for data storage
    st.session_state["times"] = []
    st.session_state["values"] = []
    st.session_state["count"] = 0
    minstep = 5
    # Load and initialize the Minsky model
    model_file = "BOMDwithGovernmentLive.mky"
    minsky.load(model_file)
    minsky.reset()
    minsky.order(4)  # 4th order Runge-Kutta
    minsky.implicit(0)  # Explicit integration
    # minsky.stepMin(minstep)
    minsky.running(True)


# Create two columns for the charts
col1, col2 = st.columns(2)

def create_charts(gdp_df, debt_df, money_df, int_df):
# Create chart containers and initial charts
    with col1:
        st.subheader("GDP")
        gdp_chart = st.line_chart(gdp_df, x_label="Years", y_label="GDP")

    with col2:
        st.subheader("Debt")
        debt_chart = st.line_chart(debt_df, x_label="Years", y_label="Debt % GDP")

    # Add a new row for Money Supply and Bank Accounts
    with col1:
        st.subheader("Money Supply and Bank Accounts")
        money_chart = st.line_chart(money_df, x_label="Years", y_label="Money")

    with col2:
        st.subheader("Interest Payments")
        int_chart = st.line_chart(int_df, x_label="Years", y_label="Interest % GDP")

    return gdp_chart, debt_chart, money_chart, int_chart


# Real-time simulation
for count in range(total_steps):  # Use the slider value for total steps
    # Get the current time and values
    current_time = minsky.t()
    # Convert simulation time to years (assuming 1 time unit = 1 year)
    current_year = current_time+1
    
    gdp_value = minsky.variableValues[":GDP"].value()
    gov_debt_percent_of_gdp = minsky.variableValues[":Gov<sub>Debt</sub><sup>%GDP</sup>"].value()
    priv_debt_percent_of_gdp = minsky.variableValues[":Priv<sub>Debt</sub><sup>%GDP</sup>"].value()
    money = minsky.variableValues[":Money"].value()
    borrowers = minsky.variableValues[":Borrowers"].value()
    savers = minsky.variableValues[":Savers"].value()
    banks = minsky.variableValues[":Banks"].value()
    gov_int_percent_of_gdp = minsky.variableValues[":Gov<sub>Int</sub><sup>%GDP</sup>"].value()
    priv_int_percent_of_gdp = minsky.variableValues[":Priv<sub>Int</sub><sup>%GDP</sup>"].value()

    # Create DataFrames with the new data
    gdp_df = pd.DataFrame({
        'GDP': [gdp_value]
    }, index=[current_year])
    
    debt_df = pd.DataFrame({
        'Gov Debt %GDP': [gov_debt_percent_of_gdp],
        'Private Debt %GDP': [priv_debt_percent_of_gdp]
    }, index=[current_year])
    
    money_df = pd.DataFrame({
        'Money': [money],
        'Savers': [savers],
        'Borrowers': [borrowers],
        'Banks': [banks]
    }, index=[current_year])
    
    int_df = pd.DataFrame({
        'Gov Int %GDP': [gov_int_percent_of_gdp],
        'Priv Int %GDP': [priv_int_percent_of_gdp]
    }, index=[current_year])
    if count == 0:
        gdp_chart, debt_chart, money_chart, int_chart = create_charts(gdp_df, debt_df, money_df, int_df)
    # Update charts only every N steps
    if st.session_state["count"] % update_freq == 0:
        with col1:
            gdp_chart.add_rows(gdp_df)
            money_chart.add_rows(money_df)
        
        with col2:
            debt_chart.add_rows(debt_df)
            int_chart.add_rows(int_df)
    
    # Step the simulation
    minsky.step()
    
    time.sleep(0.01)  # Small delay for visualization
    print("Updated", st.session_state["count"])
    st.session_state["count"] += 1
