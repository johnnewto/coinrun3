import pyminsky
from pyminsky import minsky

import matplotlib.pyplot as plt

# Initialize Minsky


# Load the Minsky model file
model_file = "BOMDwithGovernmentLive.mky"
minsky.load(model_file)
print(f"Loaded model: {model_file}")

# Set simulation parameters
minsky.setT0(0.0)  # Start time
minsky.setDt(0.1)  # Time step
minsky.setMaxTime(100.0)  # End time

# Run the simulation
minsky.reset()  # Reset model to initial conditions
minsky.run()  # Execute the simulation
print("Simulation completed")

# Extract GDP values
# Assuming 'GDP' is a variable defined in the model
time_points = minsky.getTimePoints()  # List of time points
gdp_values = minsky.getVariableValues("GDP")  # List of GDP values over time

# Verify data
if len(time_points) == len(gdp_values):
    print("Data extracted successfully")
else:
    print("Error: Mismatch in time points and GDP values")

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(time_points, gdp_values, label="GDP", color="blue")
plt.title("GDP Over Time (Minsky Model)")
plt.xlabel("Time")
plt.ylabel("GDP")
plt.grid(True)
plt.legend()
plt.savefig("gdp_simulation.png")
plt.close()
print("Plot saved as gdp_simulation.png")

# Save the simulation results to a CSV file
import pandas as pd
results = pd.DataFrame({"Time": time_points, "GDP": gdp_values})
results.to_csv("gdp_simulation_results.csv", index=False)
print("Results saved to gdp_simulation_results.csv")