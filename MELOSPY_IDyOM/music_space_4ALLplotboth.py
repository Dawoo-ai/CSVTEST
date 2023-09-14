import pandas as pd
import umap
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import warnings

def reduce_and_plot(input_file, color, label, delimiter):
    # Load data
    data = pd.read_csv(input_file, delimiter=delimiter)
    
    # Drop the 'id' column
    data = data.drop(columns='id')
    
    # Drop rows containing NaN values
    # data_cleaned = data.dropna(axis=0)

    data.fillna(data.mean(), inplace=True)

    print(f"Number of points in {label}: {data.shape[0]}")
    
    # Convert dataframe to float32 numpy array
    data_array = data.values.astype('float32')
    
    # Suppress NumbaDeprecationWarning
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        
        # Apply UMAP to reduce to 3D
        reducer = umap.UMAP(n_components=3, random_state=42)
        embedding = reducer.fit_transform(data_array)
    
    # Plot the results
    ax.scatter(embedding[:, 0], embedding[:, 1], embedding[:, 2], s=5, c=color, label=label)

# Create a figure and 3D axis
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot data from the first CSV file in red
input_file_path1 = "COMPO_1500.csv"
reduce_and_plot(input_file_path1, 'red', 'Mélodies produites P', delimiter=';')

# Plot data from the second CSV file in blue
input_file_path2 = "MS_MID1500.csv"
reduce_and_plot(input_file_path2, 'blue', 'Sous ensemble des mélodies C', delimiter=',')

# Add title and legend
ax.set_title("Représentation des deux ensembles de mélodies")
ax.legend()

# Show the plot
plt.show()
