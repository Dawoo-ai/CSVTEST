import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_data_in_3d_space(csv_filename, delimiter=";"):
    # Load data from the CSV file
    data = pd.read_csv(csv_filename, sep=delimiter)
    
    x = data['fuzzyint_zipf']
    y = data['ic_entropy']
    z = data['pc_entropy']
    midi_files = data['id'].tolist()

    # Create a 3D scatter plot
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(x, y, z, c='b', marker='o', picker=True)

    # Interactive mechanism to display the id on click
    def on_pick(event):
        ind = event.ind[0]
        ax.set_title(f"Selected ID: {midi_files[ind]}")
        fig.canvas.draw()

    fig.canvas.mpl_connect('pick_event', on_pick)

    ax.set_xlabel('Fuzzyint Zipf')
    ax.set_ylabel('IC Entropy')
    ax.set_zlabel('PC Entropy')

    plt.show()

if __name__ == "__main__":
    csv_filename = "MS_4.csv"
    delimiter_choice = input("Enter the delimiter used in the CSV (default is ';'): ")
    delimiter = delimiter_choice if delimiter_choice else ";"
    
    plot_data_in_3d_space(csv_filename, delimiter)

