import matplotlib.pyplot as plt
import seaborn as sns 


def plot_emission_data(df):
    # Unieke emissionlabels
    emissionlabels = df['emmisionlabel'].unique()
    
    # Instellen van de plot
    fig, axes = plt.subplots(nrows=len(emissionlabels), ncols=1, figsize=(10, 5 * len(emissionlabels)))
    
    if len(emissionlabels) == 1:
        axes = [axes]
    
    for ax, label in zip(axes, emissionlabels):
        subset = df[df['emmisionlabel'] == label]
        
        # Plot de product waarden
        sns.barplot(x="omschrijving", y='product', data=subset, ax=ax, color='blue', label='Product')
        
        # Maak een tweede y-as voor percentagenumber_defined
        ax2 = ax.twinx()
        sns.scatterplot(x="omschrijving", y='percentagenumber_defined', data=subset, ax=ax2, color='gray', s=100, label='Percentage Defined')
        
        # Stel de limieten van de tweede y-as in
        ax2.set_ylim(0, 100)
        ax2.grid(False)
        
        ax.set_title(f'Emission Label: {label}')
        ax.set_ylabel('Estimated Impact')
        ax.set_xlabel('Product')
        ax.legend(loc='upper left')
        ax2.set_ylabel('Percentage Defined')
        ax2.legend(loc='upper right')
    
    plt.tight_layout()
    plt.show()


def plot_data(df, product_col, variable_col, percentage_col, value_col, y_label_col, x_label, percentage_label):
    # Unieke emissionlabels
    emissionlabels = df[variable_col].unique()
    
    # Instellen van de plot
    fig, axes = plt.subplots(nrows=len(emissionlabels), ncols=1, figsize=(10, 5 * len(emissionlabels)))
    
    if len(emissionlabels) == 1:
        axes = [axes]
    
    for ax, label in zip(axes, emissionlabels):
        subset = df[df[variable_col] == label]
        
        # Plot de product waarden
        sns.barplot(x=product_col, y=value_col, data=subset, ax=ax, color='blue', label='Product')
        
        # Maak een tweede y-as voor percentage_col
        ax2 = ax.twinx()
        sns.scatterplot(x=product_col, y=percentage_col, data=subset, ax=ax2, color='gray', s=100, label='Percentage Defined')
        
        # Stel de limieten van de tweede y-as in
        ax2.set_ylim(0, 100)
        
        # Verwijder de horizontale lijnen van de tweede y-as
        ax2.grid(False)
        
        # Stel de y-as label in op basis van de y_label_col
        y_label = subset[y_label_col].iloc[0]
        
        ax.set_title(f'Emission Label: {label}')
        ax.set_ylabel(y_label)
        ax.set_xlabel(x_label)
        ax.legend(loc='upper left')
        ax2.set_ylabel(percentage_label)
        ax2.legend(loc='upper right')
    
    plt.tight_layout()
    plt.show()
