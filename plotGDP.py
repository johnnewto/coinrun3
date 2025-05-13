import sys
import matplotlib.pyplot as plt
import numpy as np
# from pathlib import Path
plt.switch_backend('TkAgg')

# # Add the parent directory to Python path to import pyminsky
# here = Path(__file__).parent
# if str(here) == "": here = '.'  # relative path
# sys.path.append(str(here))

from pyminsky import minsky

def visualize_model(model_file):
    """
    Visualize a Minsky model file showing its structure and variables.
    
    Args:
        model_file (str): Path to the .mky model file
    """
    # Load the model
    minsky.load(model_file)
    
    # Get all variables
    stocks = []
    flows = []
    parameters = []
    
    for variable_name in minsky.variableValues.keys():
        var = minsky.variableValues[variable_name]
        if var.type() == 'flow':
            flows.append(variable_name)
        elif var.type() == 'stock':
            stocks.append(variable_name)
        else:
            parameters.append(variable_name)
    
    # Variable counts
    counts = [len(stocks), len(flows), len(parameters)]
    labels = ['Stocks', 'Flows', 'Parameters']

    # Stock variables

    if stocks:
        for i, stock in enumerate(sorted(stocks)):
            print(f"Stock Variable {i+1}: {stock}")

    if flows:
        for i, flow in enumerate(sorted(flows)):
            print(f"Flow Variable {i+1}: {flow}")

    
    # Plot 4: Parameters
        for i, param in enumerate(sorted(parameters)):
            print(f"Parameter Variable {i+1}: {param}")



def plot_variable(model_file, variable_name, num_steps=8000):
    """
    Plot a stock or flow variable from a Minsky model.
    
    Args:
        model_file (str): Path to the .mky model file
        variable_name (str): Name of the variable to plot
        num_steps (int): Number of simulation steps to run
    """
    # Load and initialize the model
    minsky.load(model_file)
    minsky.reset()
    
    # Set up simulation parameters
    minsky.order(4)  # 4th order Runge-Kutta
    minsky.implicit(0)  # Explicit integration
    
    # Arrays to store time and variable values
    times = []
    values = []
    
    # Run simulation and collect data
    minsky.running(True)
    for _ in range(num_steps):
        times.append(minsky.t())
        # Get the variable value
        if variable_name in minsky.variableValues.keys():
            var = minsky.variableValues[variable_name]
            values.append(var.value())
        else:
            print(f"Variable {variable_name} not found in model")
            return
        minsky.step()
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(times, values, 'b-', linewidth=2)
    # convert sub abd sup to _ and ^
    title_name = variable_name.replace("<sub>", "_{").replace("</sub>", "}").replace("<sup>", "^{").replace("</sup>", "}")
    plt.title(f'{title_name} over time')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.grid(True)
    plt.show()
    plt.savefig("gdp_simulation.png")
    plt.close()
    print("Plot saved as gdp_simulation.png")

if __name__ == "__main__":
    # if len(sys.argv) < 3:
    #     print("Usage: python plot_minsky.py <model_file.mky> <variable_name>")
    #     sys.exit(1)
    
    # model_file = sys.argv[1]
    # variable_name = sys.argv[2]

    model_file = "BOMDwithGovernmentLive.mky"
    visualize_model(model_file)
    variable_name = ":GDP"  # Example variable name, change as needed
    # variable_name = ":Gov<sub>Debt</sub><sup>%GDP</sup>"  # Example variable name, change as needed

    print(f" {variable_name} from {model_file}")
    plot_variable(model_file, variable_name, num_steps=800)
    # print(f"Plotting {variable_name} from {model_file}")
