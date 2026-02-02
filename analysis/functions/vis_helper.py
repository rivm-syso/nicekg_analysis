import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import numpy as np
from venn import venn


def plot_four_set_venn(sets, format = "png", save_path=None, border=True):
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
        plt.savefig(save_path, format=format, dpi=400, bbox_inches='tight')
        print(f"Plot saved as {save_path}")
    else:
        # Show the plot
        plt.show()




def create_network_plot(final_usecase, output_path1="figures/lineplot.svg"):
    """
    Create network plot from final_usecase dataframe.
    
    Parameters:
    -----------
    final_usecase : pd.DataFrame
        Input dataframe
    output_path1 : str
        First save path (default: "figures/lineplot.svg")
    output_path2 : str
        Second save path (default: "psvg")
    """
    # Your data
    df = final_usecase.copy()

    # Create a directed graph
    G = nx.DiGraph()

    # Get unique taxa and assign colors
    unique_taxa = df['ncbilabel'].unique()
    taxon_colors = plt.cm.Set3(np.linspace(0, 1, len(unique_taxa)))
    taxon_color_map = {taxon: taxon_colors[i] for i, taxon in enumerate(unique_taxa)}

    # Separate data into ingredient data and other datasets
    ingredient_data = df[df['dataavailable'] == 'Ingredient data available']
    other_data = df[df['dataavailable'] != 'Ingredient data available']

    # Add ingredient data nodes (level 0) with edges to query class (level 1)
    for idx, row in ingredient_data.iterrows():
        dataset = row['datasetlabel']
        queryclasslabel = row['queryclasslabel']
        ncbilabel = row['ncbilabel']
        
        dataset_unique = f"ingredient_{dataset}_{idx}"
        
        G.add_node(dataset_unique, level=0, node_type='ingredient', label=dataset, taxon=ncbilabel)
        G.add_node(queryclasslabel, level=1, node_type='class', label=queryclasslabel, taxon=ncbilabel)
        
        G.add_edge(dataset_unique, queryclasslabel)

    # Add other dataset nodes (level 2) with edges from query class (level 1)
    for idx, row in other_data.iterrows():
        dataset = row['datasetlabel']
        queryclasslabel = row['queryclasslabel']
        ncbilabel = row['ncbilabel']
        datatype = row['dataavailable']
        
        dataset_unique = f"other_{dataset}_{idx}"
        datatype_node = f"datatype_{datatype}"
        
        G.add_node(queryclasslabel, level=1, node_type='class', label=queryclasslabel, taxon=ncbilabel)
        G.add_node(dataset_unique, level=2, node_type='other', label=dataset, taxon=ncbilabel)
        G.add_node(datatype_node, level=3, node_type='datatype', label=datatype)
        
        G.add_edge(queryclasslabel, dataset_unique)
        G.add_edge(dataset_unique, datatype_node)

    # Create hierarchical layout with closer columns
    pos = nx.multipartite_layout(G, subset_key='level', align='vertical', scale=1)

    # Sort nodes by taxon within each level
    # Create a mapping of taxon to a sort order
    taxon_order = {taxon: i for i, taxon in enumerate(sorted(unique_taxa))}

    # Group nodes by level and sort by taxon
    for level in range(4):
        level_nodes = [n for n in G.nodes() if G.nodes[n]['level'] == level]
        
        # Sort nodes by taxon (if they have taxon attribute)
        sorted_nodes = sorted(level_nodes, key=lambda n: (
            taxon_order.get(G.nodes[n].get('taxon', ''), 999),  # Sort by taxon first
            G.nodes[n].get('label', '')  # Then by label for consistent ordering within taxon
        ))
        
        # Reassign y-positions based on sorted order
        if sorted_nodes:
            y_positions = np.linspace(-len(sorted_nodes)/2, len(sorted_nodes)/2, len(sorted_nodes))
            for i, node in enumerate(sorted_nodes):
                pos[node] = (pos[node][0], y_positions[i])

    # Manually adjust positions to increase spacing
    for node in pos:
        level = G.nodes[node]['level']
        if level == 0:  # Ingredient level
            pos[node] = (pos[node][0], pos[node][1] * 2.0)
        elif level == 1:  # Query class level
            pos[node] = (pos[node][0], pos[node][1] * 2.5)
        elif level == 2:  # Other datasets level
            pos[node] = (pos[node][0], pos[node][1] * 2.0)
        elif level == 3:  # Data type level - increased spacing
            pos[node] = (pos[node][0], pos[node][1] * 3.5)

    # Create figure
    fig, ax = plt.subplots(figsize=(17, 20), facecolor ="none")
    ax.set_facecolor('none')

    # Draw ingredient nodes with taxon colors
    for node in G.nodes():
        node_data = G.nodes[node]
        if node_data.get('node_type') == 'ingredient':
            taxon = node_data.get('taxon')
            node_color = taxon_color_map[taxon]
            nx.draw_networkx_nodes(G, pos, nodelist=[node], 
                                  node_color=[node_color], 
                                  node_size=1200,
                                  alpha=0.9,
                                  ax=ax)

    # Draw class nodes with taxon colors
    for node in G.nodes():
        node_data = G.nodes[node]
        if node_data.get('node_type') == 'class':
            taxon = node_data.get('taxon')
            node_color = taxon_color_map[taxon]
            nx.draw_networkx_nodes(G, pos, nodelist=[node], 
                                  node_color=[node_color], 
                                  node_size=1200,
                                  alpha=0.9,
                                  ax=ax)

    # Draw other dataset nodes with taxon colors
    for node in G.nodes():
        node_data = G.nodes[node]
        if node_data.get('node_type') == 'other':
            taxon = node_data.get('taxon')
            node_color = taxon_color_map[taxon]
            nx.draw_networkx_nodes(G, pos, nodelist=[node], 
                                  node_color=[node_color], 
                                  node_size=1200,
                                  alpha=0.9,
                                  ax=ax)

    # Draw data type nodes (neutral color)
    datatype_nodes = [n for n, d in G.nodes(data=True) if d.get('node_type') == 'datatype']
    nx.draw_networkx_nodes(G, pos, nodelist=datatype_nodes, 
                          node_color='#FFE66D', 
                          node_size=1200,
                          alpha=0.9,
                          ax=ax,
                          edgecolors='black',
                          linewidths=1.5)

    # Draw edges with different widths based on connectivity
    # First, identify edges that are part of complete paths (ingredient -> class -> other -> datatype)
    complete_path_edges = set()

    for idx, row in other_data.iterrows():
        queryclasslabel = row['queryclasslabel']
        dataset = row['datasetlabel']
        datatype = row['dataavailable']
        
        dataset_unique = f"other_{dataset}_{idx}"
        datatype_node = f"datatype_{datatype}"
        
        # Check if this query class has incoming edges from ingredient nodes
        has_ingredient = False
        for pred in G.predecessors(queryclasslabel):
            if G.nodes[pred].get('node_type') == 'ingredient':
                has_ingredient = True
                # Add the ingredient -> class edge to complete path
                complete_path_edges.add((pred, queryclasslabel))
                break
        
        if has_ingredient:
            # Add all edges in this path to complete path set
            complete_path_edges.add((queryclasslabel, dataset_unique))
            complete_path_edges.add((dataset_unique, datatype_node))

    # Draw regular edges first (thinner)
    regular_edges = [e for e in G.edges() if e not in complete_path_edges]
    nx.draw_networkx_edges(G, pos, 
                           edgelist=regular_edges,
                           edge_color='#CCCCCC',
                           arrows=False,
                      
                           width=3,
                           alpha=0.7,
                           ax=ax,
                           connectionstyle='arc3,rad=0.1')

    # Draw complete path edges (thicker)
    nx.draw_networkx_edges(G, pos, 
                           edgelist=list(complete_path_edges),
                           edge_color='#666666',
                           arrows=False,
                  
                           width=3.0,
                           alpha=0.7,
                           ax=ax,
                           connectionstyle='arc3,rad=0.1')

    # Draw labels
    labels = {node: G.nodes[node].get('label', node) for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, 
                            labels=labels,
                            font_size=13,
                            font_weight='bold',
                            ax=ax)

    # Add legend for taxa
    legend_elements = []
    for taxon in unique_taxa:
        legend_elements.append(
            plt.Line2D([0], [0], marker='o', color='w', 
                       markerfacecolor=taxon_color_map[taxon], markersize=12, 
                       label=taxon, markeredgecolor='black', markeredgewidth=1)
        )

    # Add separator and column descriptions
    legend_elements.append(plt.Line2D([0], [0], color='none', label=''))


    # Add edge description to legend
    legend_elements.append(plt.Line2D([0], [0], color='none', label=''))
    legend_elements.append(plt.Line2D([0], [0], color='#666666', linewidth=1.5, 
                           label='Ingredient information available in dataset'))
    legend_elements.append(plt.Line2D([0], [0], color='#CCCCCC', linewidth=1.5, 
                           label='Partial path'))

    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.2, 1) , fontsize=12, framealpha=0.9)

    plt.title('Food Ingredient Network: Four-Column View by NCBI Taxon', 
              fontsize=18, fontweight='bold', pad=20)


    # Set axis limits to include all content with extra padding
    all_x = [pos[node][0] for node in pos]
    all_y = [pos[node][1] for node in pos]
    x_margin = (max(all_x) - min(all_x)) * 0.1  # 15% margin
    y_margin = (max(all_y) - min(all_y)) * 0.08  # 8% margin
    ax.set_xlim(min(all_x) - x_margin, max(all_x) + x_margin)
    ax.set_ylim(min(all_y) - y_margin, max(all_y) + y_margin)


    plt.axis('off')
    plt.tight_layout(pad = 1)
    plt.savefig(output_path1, format = "svg", dpi = 300, bbox_inches = "tight", transparent = True, facecolor = None)
    plt.show()


    # Print some network statistics
    print(f"Network Statistics:")
    print(f"Total nodes: {G.number_of_nodes()}")
    print(f"Total edges: {G.number_of_edges()}")
    print(f"\nNode counts by type:")
    for node_type in ['ingredient', 'class', 'other', 'datatype']:
        count = len([n for n, d in G.nodes(data=True) if d.get('node_type') == node_type])
        print(f"  {node_type}: {count}")
    print(f"\nTaxa represented: {', '.join(unique_taxa)}")