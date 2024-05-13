import networkx as nx
import matplotlib.pyplot as plt

class CommunicationVisualization:
    def __init__(self, brain_regions):
        self.brain_regions = brain_regions

    def plot_communication(self, communication_data):
        # Create a directed graph
        G = nx.DiGraph()

        # Add brain regions as nodes
        for region in self.brain_regions:
            G.add_node(region)

        # Add communication edges between brain regions
        for sender, receivers in communication_data.items():
            for receiver in receivers:
                G.add_edge(sender, receiver)

        # Define positions for nodes
        pos = nx.spring_layout(G)

        # Draw the graph
        plt.figure(figsize=(10, 6))
        nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=12, font_weight="bold", arrowsize=20)
        plt.title("Brain Communication Visualization")
        plt.show()

def start_communication_visualization(communication_data, brain_regions):
    visualization = CommunicationVisualization(brain_regions)
    visualization.plot_communication(communication_data)