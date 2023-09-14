import pandas as pd
import umap
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import warnings
import numpy as np
import scipy.io

def reduce_and_plot(main_file, ic_file):
    # Load main data
    data = pd.read_csv(main_file, delimiter=',')
    
    # Remove rows containing NaN values
    data = data.dropna()
    
    # Extract filenames from the 'id' column in the main dataset
    data['Filename'] = data['id'].str.split('/').str[-1]
    
    # Drop non-numeric columns from the main dataset
    data_for_umap = data.drop(columns=['id', 'Filename'])
    
    # Convert dataframe to float32 numpy array
    data_array = data_for_umap.values.astype('float32')
    
    # Load information content data from .mat file
    ic_data_mat = scipy.io.loadmat(ic_file)
    ic_averaged = [np.mean(item[0]) for item in ic_data_mat['ic'][0]]
    
    # Trim the ic_averaged list to match the size of the cleaned data
    ic_averaged = ic_averaged[:len(data)]
    
    ic_averaged_df = pd.DataFrame(ic_averaged, columns=['Average Information Content'])
    
    # Merge datasets on index using an outer join
    merged_data = pd.merge(data, ic_averaged_df, left_index=True, right_index=True, how='outer')
    
    # Extract information content values for coloring
    colors = merged_data['Average Information Content'].values
    
    # Ensure the colors array is trimmed to match the size of the data_array
    colors = colors[:len(data_array)]
    
    # Suppress NumbaDeprecationWarning
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        
        # Apply UMAP to reduce to 3D
        reducer = umap.UMAP(n_components=3, random_state=42)
        embedding = reducer.fit_transform(data_array)
    
    # Normalize the colors for the plot (ignoring NaN values)
    norm = plt.Normalize(np.nanmin(colors), np.nanmax(colors))
    
    # Create a 3D scatter plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(embedding[:, 0], embedding[:, 1], embedding[:, 2], 
                    c=colors, marker='o', picker=True, cmap="viridis", norm=norm, edgecolors='w')

    # Add colorbar for the information content values
    cbar = fig.colorbar(sc, ax=ax)
    cbar.set_label('Average Information Content')
    
    # List of midi filenames
    midi_files = merged_data['Filename'].values

    # Interactive mechanism to display the id on click
    def on_pick(event):
        ind = event.ind[0]
        ax.set_title(f"Selected ID: {midi_files[ind]}")
        fig.canvas.draw()

    fig.canvas.mpl_connect('pick_event', on_pick)
    
    plt.show()

# Usage
if __name__ == "__main__":
    main_file_path = "MS_4_ALL_15k_smallgpt - MS_4_ALL_15k_smallgpt.csv.csv"
    ic_file_path = "/home/dxwoo/Téléchargements/outputs_in_mat/ic.mat"
    reduce_and_plot(main_file_path, ic_file_path)