# import sys
import matplotlib.pyplot as plt
import matplotlib
# import time
# import numpy as np
from pathlib import Path
import tkinter as tk
# plt.ion()
matplotlib.use('TkAgg')
# Add the parent directory to Python path to import pyminsky
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

    
    # Create a figure with subplots
    fig = plt.figure(figsize=(15, 10))
    
    # Plot 1: Variable counts
    ax1 = plt.subplot(221)
    counts = [len(stocks), len(flows), len(parameters)]
    labels = ['Stocks', 'Flows', 'Parameters']
    ax1.bar(labels, counts)
    ax1.set_title('Variable Types Distribution')
    ax1.set_ylabel('Count')
    
    # Plot 2: Stock variables
    ax2 = plt.subplot(222)
    if stocks:
        ax2.text(0.1, 0.9, 'Stock Variables:', fontsize=12, fontweight='bold')
        for i, stock in enumerate(sorted(stocks)):
            ax2.text(0.1, 0.8 - i*0.05, f'• {stock}', fontsize=10)
    else:
        ax2.text(0.1, 0.5, 'No stock variables', fontsize=10)
    ax2.axis('off')
    
    # Plot 3: Flow variables
    ax3 = plt.subplot(223)
    if flows:
        ax3.text(0.1, 0.9, 'Flow Variables:', fontsize=12, fontweight='bold')
        for i, flow in enumerate(sorted(flows)):
            ax3.text(0.1, 0.8 - i*0.05, f'• {flow}', fontsize=10)
    else:
        ax3.text(0.1, 0.5, 'No flow variables', fontsize=10)
    ax3.axis('off')
    
    # Plot 4: Parameters
    ax4 = plt.subplot(224)
    if parameters:
        ax4.text(0.1, 0.9, 'Parameters:', fontsize=12, fontweight='bold')
        for i, param in enumerate(sorted(parameters)):
            ax4.text(0.1, 0.8 - i*0.05, f'• {param}', fontsize=10)
    else:
        ax4.text(0.1, 0.5, 'No parameters', fontsize=10)
    ax4.axis('off')
    
    plt.suptitle(f'Minsky Model Structure: {Path(model_file).name}', fontsize=14)
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    # Create a Tkinter window
    root = tk.Tk()
    root.title("Minsky GDP Plot")
    model_file = "BOMDwithGovernmentLive.mky"
    # variable_name = ":GDP"  # Example variable name, change as needed
    # plot_variable(model_file, variable_name)
    # print(f"Plotting {variable_name} from {model_file}")
    visualize_model(model_file) 
    root.mainloop()

    # Clean up
    plt.close()