import matplotlib.pyplot as plt
import networkx as nx

# Create a directed graph
G = nx.DiGraph()

# Add input nodes
input_nodes = ["I$_1$", "I$_2$", "I$_{719}$", "I$_{720}$"]

# Add first hidden layer nodes
hidden_layer_1 = ["H$_{1,1}$", "H$_{1,2}$", "H$_{1,62}$", "H$_{1,63}$"]

# Add second hidden layer nodes
hidden_layer_2 = ["H$_{2,1}$", "H$_{2,2}$", "H$_{2,31}$", "H$_{2,32}$"]

# Define all output nodes
output_nodes = ["O$_1$", "O$_2$", "O$_{59}$", "O$_{60}$"]

# Add all nodes to the graph
G.add_nodes_from(input_nodes, layer="input")
G.add_nodes_from(hidden_layer_1, layer="hidden_1")
G.add_nodes_from(hidden_layer_2, layer="hidden_2")
G.add_nodes_from(output_nodes, layer="output")

# Function to connect layers
def connect_layers(source_nodes, dest_nodes):
    for src in source_nodes:
        for dest in dest_nodes:
            G.add_edge(src, dest)

# Connect input nodes to first hidden layer
connect_layers(input_nodes, hidden_layer_1)

# Connect first hidden layer to second hidden layer
connect_layers(hidden_layer_1, hidden_layer_2)

# Connect second hidden layer to output layer
connect_layers(hidden_layer_2, output_nodes)

# Define positions for nodes
pos = {}

# Manually define positions for input nodes with increased spacing
pos["I$_1$"] = (0, 1.0)  # Place I_1
pos["I$_2$"] = (0, 0.7)  # Place I_2
pos["I$_{719}$"] = (0, 0.2)  # Add a gap below I_2
pos["I$_{720}$"] = (0, -0.1)  # Place I_720 slightly below I_719

# Manually define positions for the first hidden layer with the required constraints
pos["H$_{1,1}$"] = (5, 1.2)  # H1,1 is higher than I1
pos["H$_{1,2}$"] = (5, 0.9)  # H1,2 below H1,1
pos["H$_{1,62}$"] = (5, 0.1)  # H1,62 below H1,2 with a large gap
pos["H$_{1,63}$"] = (5, -0.2)  # H1,63 below H1,62 with a small gap

# Manually define positions for the second hidden layer with the required constraints
pos["H$_{2,1}$"] = (10, 1.2)  # H2,1 is higher than H2,2
pos["H$_{2,2}$"] = (10, 0.9)  # H2,2 below H2,1
pos["H$_{2,31}$"] = (10, 0.1)  # H2,31 below H2,2 with a large gap
pos["H$_{2,32}$"] = (10, -0.2)  # H2,32 below H2,31 with a small gap

# Manually define positions for the output layer with adjusted vertical positions
pos["O$_1$"] = (15, 1.0)  # Adjust O1 to not align with other layers
pos["O$_2$"] = (15, 0.7)  # Adjust O2 below O1
pos["O$_{59}$"] = (15, 0.2)  # Adjust O59 below O2 with a gap
pos["O$_{60}$"] = (15, -0.1)  # Adjust O60 below O59 with a small gap

# Function to arrange nodes vertically with x-offset and spacers
def set_layer_positions(nodes, x_offset, start_y=1.0, spacing=0.3):
    y = start_y
    for node in nodes:
        if node not in pos:  # Skip manually positioned nodes
            pos[node] = (x_offset, y)
            y -= spacing

# Set positions for output layer independently
set_layer_positions(output_nodes, x_offset=15, start_y=0.8, spacing=0.3)  # Output layer

# Adjust figure size and layout
plt.figure(figsize=(10, 5))  # Adjust the figure size
plt.axis("off")  # Turn off axes for better appearance

# Draw the graph
nx.draw(
    G,
    pos,
    with_labels=True,
    node_color=[
        "lightblue" if node in input_nodes else
        "lightgreen" if node in hidden_layer_1 + hidden_layer_2 else
        "lightcoral"
        for node in G.nodes
    ],
    node_size=3000,
    font_size=10,
    edge_color="gray"
)

# Manually adjust plot limits to enforce proper spacing
plt.ylim(-0.5, 1.5)  # Adjust vertical limits for better spacing
plt.tight_layout()
plt.show()
