import matplotlib.pyplot as plt
from venn import venn


def plot_four_set_venn(sets, labels=None, save_path=None, border=True):
    """
    Plots a Venn-like diagram for 4 sets using the venn package and saves as an SVG with optional border.

    Parameters:
    - sets: A dictionary where keys are labels and values are sets.
    - labels: A list of labels for the sets. Defaults to None, which will use dictionary keys.
    - save_path: Path to save the SVG file. If None, the plot is shown but not saved.
    - border: Add a border around the SVG if True. Defaults to True.

    Returns:
    - None
    """
    if len(sets) != 4:
        raise ValueError("This function is designed for exactly 4 sets.")

    # Create the Venn diagram plot
    plt.figure(figsize=(4, 4))  # Set size of the figure
    venn(sets)

    if border:
        # Add a border by modifying the limits of the figure
        plt.gca().spines['top'].set_visible(True)
        plt.gca().spines['left'].set_visible(True)
        plt.gca().spines['right'].set_visible(True)
        plt.gca().spines['bottom'].set_visible(True)
        # Optionally customize border style (color, linewidth, etc.)
        # for spine in plt.gca().spines.values():
        # spine.set_edgecolor('black')
        # spine.set_linewidth(0.3)

    if save_path is not None:
        # Save plot as SVG
        plt.savefig(save_path, format='png', dpi=400, bbox_inches='tight')
        print(f"Plot saved as {save_path}")
    else:
        # Show the plot
        plt.show()
