import os
import csv
from collections import defaultdict

def process_csv_file(file_path):
    # Read the file content
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        key_info = next(reader)  # read key information
        header = next(reader)  # skip header
        rows = [row for row in reader]

    # Process the data
    time_to_chords = defaultdict(list)
    for row in rows:
        time = row[0]
        pitch = row[1]
        # Add pitch to the list of chords for that time
        time_to_chords[time].append(pitch)

    # Sort the chords for each time
    for time, chords in time_to_chords.items():
        chords.sort()

    # Write back to the file
    with open(file_path, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(key_info)  # Write key information
        writer.writerow(["Time", "Chords"])  # Write header
        for time, chords in time_to_chords.items():
            writer.writerow([time, ' '.join(chords)])


def main():
    directory = "/home/dxwoo/Documents/Code_2/MIDIPROCESS/MIDIPROCESS/MUSICAL_SPACE/MS_2_csv"
    
    for file_name in os.listdir(directory):
        if file_name.endswith(".csv"):
            process_csv_file(os.path.join(directory, file_name))

if __name__ == '__main__':
    main()
