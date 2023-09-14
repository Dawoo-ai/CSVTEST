import os
import csv
import matplotlib.pyplot as plt

def replace_with_fundamental(csv_data):
    """ 
    Replace occurrences of notes in chords with the fundamental note 
    and return the processed data.
    """
    time_dict = {}
    for row in csv_data:
        time = row[0]
        if time not in time_dict:
            time_dict[time] = []
        time_dict[time].append(row)

    processed_data = []
    for time, notes in time_dict.items():
        if len(notes) > 1:  # We've identified a chord
            fundamental_note = min(notes, key=lambda x: x[1])[1]  # Use the lowest note as fundamental
            for note in notes:
                processed_data.append([time, fundamental_note, note[2], note[3]])
        else:
            processed_data.append(notes[0])

    return processed_data

###         FIRST 5

def plot_trajectory_from_csv(directory, num_files=2):
    """ 
    Read the first 'num_files' CSV files in the given directory 
    and plot the trajectories.
    """
    plotted_files = 0
    for csv_file in sorted(os.listdir(directory)):
        if plotted_files >= num_files:
            break
        
        if csv_file.endswith('.csv'):
            with open(os.path.join(directory, csv_file), 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip the header
                data = list(reader)
                data = [[float(row[0]), float(row[1]), float(row[2]), float(row[3])] for row in data]
                processed_data = replace_with_fundamental(data)

                times = [row[0] for row in processed_data]
                pitches = [row[1] for row in processed_data]
                plt.plot(times, pitches, label=csv_file)
                
                plotted_files += 1

    plt.xlabel('Time')
    plt.ylabel('Pitch')
    plt.legend(loc='best')
    plt.show()



###         ALL
# def plot_trajectory_from_csv(directory):
#     """ Read all CSV files in the given directory and plot the trajectories """
#     for csv_file in os.listdir(directory):
#         if csv_file.endswith('.csv'):
#             with open(os.path.join(directory, csv_file), 'r') as f:
#                 reader = csv.reader(f)
#                 next(reader)  # Skip the header
#                 data = list(reader)
#                 data = [[float(row[0]), float(row[1]), float(row[2]), float(row[3])] for row in data]
#                 processed_data = replace_with_fundamental(data)

#                 times = [row[0] for row in processed_data]
#                 pitches = [row[1] for row in processed_data]
#                 plt.plot(times, pitches, label=csv_file)

#     plt.xlabel('Time')
#     plt.ylabel('Pitch')
#     plt.legend(loc='best')
#     plt.show()

# Plot trajectories
plot_trajectory_from_csv('MS_1_csv')
