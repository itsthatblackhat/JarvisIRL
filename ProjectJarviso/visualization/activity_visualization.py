# visualization/activity_visualization.py

import matplotlib.pyplot as plt

class ActivityVisualization:
    def __init__(self, brain_regions):
        self.brain_regions = brain_regions

    def plot_activity(self, activity_data):
        fig, ax = plt.subplots(figsize=(10, 6))

        # Define colors for each brain region
        region_colors = {
            "cerebrum": "blue",
            "cerebellum": "green",
            "brainstem": "red",
            "thalamus": "purple",
            "hypothalamus": "orange",
            "basal_ganglia": "yellow",
            "limbic": "cyan",
            "reticular": "magenta"
        }

        # Plot activity for each brain region
        for region, activity in activity_data.items():
            ax.plot(activity, label=region, color=region_colors.get(region, "black"))

        ax.set_title("Brain Activity Visualization")
        ax.set_xlabel("Time")
        ax.set_ylabel("Activity Level")
        ax.legend()
        plt.show()

def start_activity_visualization(activity_data, brain_regions):
    visualization = ActivityVisualization(brain_regions)
    visualization.plot_activity(activity_data)