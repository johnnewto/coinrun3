import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from pathlib import Path
from datetime import datetime
plt.switch_backend('TkAgg')
# Add the parent directory to Python path to import pyminsky
# here = Path(__file__).parent
# if str(here) == "": here = '.'  # relative path
# sys.path.append(str(here))

from pyminsky import minsky

class GDPPlotter:
    def __init__(self, model_file, gdp_var_name, max_points=100):
        """
        Initialize the GDP plotter.
        
        Args:
            model_file (str): Path to the .mky model file
            gdp_var_name (str): Name of the GDP variable in the model
            max_points (int): Maximum number of points to display in the plot
        """
        self.model_file = model_file
        self.gdp_var_name = gdp_var_name
        self.max_points = max_points
        
        # Load the model
        minsky.load(model_file)
        minsky.reset()
        
        # Set up simulation parameters
        minsky.order(4)  # 4th order Runge-Kutta
        minsky.implicit(0)  # Explicit integration
        minsky.running(True)
        
        # Initialize data storage
        self.times = []
        self.gdp_values = []
        
        # Set up the plot
        plt.ion()  # Enable interactive mode
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.line, = self.ax.plot([], [], 'b-', label='GDP')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('GDP')
        self.ax.set_title('Real-time GDP Plot')
        self.ax.grid(True)
        self.ax.legend()
        
    def update_plot(self):
        """Update the plot with new GDP data."""
        # Run simulation step
        minsky.step()
        
        # Get current time and GDP value
        current_time = minsky.t()
        current_gdp = minsky.variableValues[self.gdp_var_name].value()
        
        # Add new data point
        self.times.append(current_time)
        self.gdp_values.append(current_gdp)
        
        # Keep only the last max_points
        if len(self.times) > self.max_points:
            self.times = self.times[-self.max_points:]
            self.gdp_values = self.gdp_values[-self.max_points:]
        
        # Update plot data
        self.line.set_data(self.times, self.gdp_values)
        
        # Adjust plot limits
        self.ax.relim()
        self.ax.autoscale_view()
        
        # Add timestamp
        self.ax.set_title(f'Real-time GDP Plot - {datetime.now().strftime("%H:%M:%S")}')
        
        # Force redraw
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
    
    def run(self):
        """Run the real-time plot animation."""
        try:
            while True:
                self.update_plot()
                plt.pause(0.01)  # Update every 100ms
        except KeyboardInterrupt:
            print("\nStopping simulation...")
            minsky.running(False)
            plt.close()

def main():
    # if len(sys.argv) < 3:
    #     print("Usage: python plot_gdp_realtime.py <model_file.mky> <gdp_variable_name>")
    #     sys.exit(1)
    
    # model_file = sys.argv[1]
    # gdp_var_name = sys.argv[2]
    
    model_file = "BOMDwithGovernmentLive.mky"
    variable_name = ":GDP"  # Example variable name, change as needed
    plotter = GDPPlotter(model_file, variable_name)
    plotter.run()

if __name__ == "__main__":
    main() 