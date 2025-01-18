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

# Define positions for nodes with reduced horizontal spacing
pos = {}

# Manually define positions for input nodes (reduce horizontal spacing even more)
pos["I$_1$"] = (0, 1.0)
pos["I$_2$"] = (0, 0.7)
pos["I$_{719}$"] = (0, 0.2)
pos["I$_{720}$"] = (0, -0.1)

# Redefine positions for the first hidden layer (further reduce horizontal spacing)
pos["H$_{1,1}$"] = (0.5, 1.2)
pos["H$_{1,2}$"] = (0.5, 0.9)
pos["H$_{1,62}$"] = (0.5, 0.1)
pos["H$_{1,63}$"] = (0.5, -0.2)

# Redefine positions for the second hidden layer (further reduce horizontal spacing)
pos["H$_{2,1}$"] = (1, 1.2)
pos["H$_{2,2}$"] = (1, 0.9)
pos["H$_{2,31}$"] = (1, 0.1)
pos["H$_{2,32}$"] = (1, -0.2)

# Redefine positions for the output layer (further reduce horizontal spacing)
pos["O$_1$"] = (1.5, 1.0)
pos["O$_2$"] = (1.5, 0.7)
pos["O$_{59}$"] = (1.5, 0.2)
pos["O$_{60}$"] = (1.5, -0.1)

# Function to arrange nodes vertically with x-offset and spacers (again for final adjustments)
def set_layer_positions(nodes, x_offset, start_y=1.0, spacing=0.3):
    y = start_y
    for node in nodes:
        if node not in pos:  # Skip manually positioned nodes
            pos[node] = (x_offset, y)
            y -= spacing

# Apply the final position settings
set_layer_positions(output_nodes, x_offset=3, start_y=0.8, spacing=0.3)


state_l = 0.9
state_h = 3

m_left = 0.18
m_right = 0.98
m_bottom = 0.17
m_top = 0.99

plt_h = 2.5
plt_w = 3.5
# Replot the graph with even more reduced horizontal spacing
fig = plt.figure(figsize=(plt_w,plt_h))
ax2 = fig.add_subplot(1, 1, 1 )
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
    node_size=500,
    font_size=8,
    edge_color="gray"
)

# Manually adjust plot limits to enforce proper spacing
plt.ylim(-0.5, 1.5)  # Adjust vertical limits for better spacing
#plt.tight_layout()
plt.subplots_adjust(left=m_left, right=m_right, top=m_top, bottom=m_bottom, wspace=0.00, hspace= 0.0 )
plt.savefig( 'first_NN.png', dpi = 600, transparent = True )
plt.show()
