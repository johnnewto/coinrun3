import sys
import matplotlib.pyplot as plt
import networkx as nx
from pathlib import Path

# Add the parent directory to Python path to import pyminsky
here = Path(__file__).parent
if str(here) == "": here = '.'  # relative path
sys.path.append(str(here))

from pyminsky import minsky

def visualize_wiring(model_file):
    """
    Visualize the wiring diagram of a Minsky model.
    
    Args:
        model_file (str): Path to the .mky model file
    """
    # Load the model
    minsky.load(model_file)
    
    # Create a directed graph
    G = nx.DiGraph()
    
    # Add nodes and edges based on variable connections
    # for name, var in minsky.variableValues.items():
    for variable_name in minsky.variableValues.keys():
        var = minsky.variableValues[variable_name]
        # Add node with type information
        node_type = var.type()
        G.add_node(variable_name, type=node_type)

     # Add edges based on wires in the model
    for wire in minsky.model.findWire.items():
        from_var = wire.from_().item().name()
        to_var = wire.to_().item().name()
        G.add_edge(from_var, to_var)
    # # Add edges based on wires in the model
    # for wire in minsky.model.findWire(":GDP"):
    #     from_var = wire.from_().item().name()
    #     to_var = wire.to_().item().name()
    #     G.add_edge(from_var, to_var)
    
    # Create the plot
    plt.figure(figsize=(15, 10))
    
    # Use different colors for different node types
    node_colors = {
        'stock': 'lightblue',
        'flow': 'lightgreen',
        'parameter': 'lightyellow',
        'constant': 'lightgray'
    }
    
    # Get node colors based on type
    node_color_list = [node_colors.get(G.nodes[node]['type'], 'white') for node in G.nodes()]
    
    # Use spring layout for better visualization
    pos = nx.spring_layout(G, k=1, iterations=50)
    
    # Draw the network
    nx.draw_networkx_nodes(G, pos, node_color=node_color_list, node_size=2000)
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=20)
    nx.draw_networkx_labels(G, pos, font_size=8)
    
    # Add legend
    legend_elements = [plt.Line2D([0], [0], marker='o', color='w', 
                                 markerfacecolor=color, label=type_name, markersize=15)
                      for type_name, color in node_colors.items()]
    plt.legend(handles=legend_elements, loc='upper right')
    
    plt.title(f'Wiring Diagram: {Path(model_file).name}', fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    root.title("Minsky wiring Plot")
    model_file = "BOMDwithGovernmentLive.mky"

    visualize_wiring(model_file) 