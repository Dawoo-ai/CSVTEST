import os
import csv
from tegridy_tools import TMIDI

def extract_midi_data_using_tegridy(midi_file_path):
    """
    Extract the desired data from the MIDI file using tegridy_tools.
    Returns a list of tuples with format (t, p, a, d).
    """
    midi_data = []

    # Load the MIDI file using tegridy_tools
    with open(midi_file_path, 'rb') as mf:
        score = TMIDI.midi2score(mf.read())

    # Iterate through the score to extract the necessary data
    for itrack in range(1, len(score)):  # Skipping the first element which is the ticks value
        for event in score[itrack]:
            if event[0] == 'note':
                t = event[1]  # temporal dimension (start_time)
                d = event[2]  # duration dimension
                p = event[4]  # pitch dimension
                a = event[5] / 127.0  # amplitude dimension normalized
                midi_data.append((t, p, a, d))

    return midi_data

def main():
    # Directory containing MIDI files
    midi_dir = '/home/dxwoo/Documents/Code_2/MIDIPROCESS/MIDIPROCESS/MUSICAL_SPACE/MID100'

    # Directory to save the CSV files
    csv_dir = 'MS_1_csv'
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)

    # Process each MIDI file in the directory
    for file in os.listdir(midi_dir):
        if file.endswith('.mid') or file.endswith('.midi'):
            midi_data = extract_midi_data_using_tegridy(os.path.join(midi_dir, file))

            # Define the output CSV file name based on the MIDI file name
            csv_filename = os.path.splitext(file)[0] + '.csv'
            csv_filepath = os.path.join(csv_dir, csv_filename)

            # Write data for this MIDI file to the CSV
            with open(csv_filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Time', 'Pitch', 'Amplitude', 'Duration'])
                for data in midi_data:
                    writer.writerow(data)

if __name__ == "__main__":
    main()
