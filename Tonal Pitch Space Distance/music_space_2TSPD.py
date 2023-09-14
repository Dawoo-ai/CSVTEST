import csv
import os

def parse_csv(file_path):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        key = next(reader)[1]  # Extract key from the first row
        chords_data = [row for row in csv.DictReader(f)]  # Extract the rest as chord data
    return key, chords_data


def flat_to_sharp(key):
    """Converts a flat notation to sharp notation."""
    mapping = {
        "C-": "B",
        "D-": "C#",
        "E-": "D#",
        "F-": "E",
        "G-": "F#",
        "A-": "G#",
        "B-": "A#"
    }
    return mapping.get(key, key)

def get_diatonic_scale(full_key):
    # Extract the note and tonality (major/minor) from the full key string
    note, tonality = full_key.split(maxsplit=1)
    
    # Convert flat notation to sharp if necessary
    note = flat_to_sharp(note)
    # Mapping of major and minor keys to their diatonic scales
    major_scales = {
        "C": [0, 2, 4, 5, 7, 9, 11],
        "C#": [1, 3, 5, 6, 8, 10, 0],
        "D": [2, 4, 6, 7, 9, 11, 1],
        "D#": [3, 5, 7, 8, 10, 0, 2],
        "E": [4, 6, 8, 9, 11, 1, 3],
        "F": [5, 7, 9, 10, 0, 2, 4],
        "F#": [6, 8, 10, 11, 1, 3, 5],
        "G": [7, 9, 11, 0, 2, 4, 6],
        "G#": [8, 10, 0, 1, 3, 5, 7],
        "A": [9, 11, 1, 2, 4, 6, 8],
        "A#": [10, 0, 2, 3, 5, 7, 9],
        "B": [11, 1, 3, 4, 6, 8, 10]
    }
    
    minor_scales = {
        "C": [0, 2, 3, 5, 7, 8, 10],
        "C#": [1, 3, 4, 6, 8, 9, 11],
        "D": [2, 4, 5, 7, 9, 10, 0],
        "D#": [3, 5, 6, 8, 10, 11, 1],
        "E": [4, 6, 7, 9, 11, 0, 2],
        "F": [5, 7, 8, 10, 0, 1, 3],
        "F#": [6, 8, 9, 11, 1, 2, 4],
        "G": [7, 9, 10, 0, 2, 3, 5],
        "G#": [8, 10, 11, 1, 3, 4, 6],
        "A": [9, 11, 0, 2, 4, 5, 7],
        "A#": [10, 0, 1, 3, 5, 6, 8],
        "B": [11, 1, 2, 4, 6, 7, 9]
    }
    
    if "major" in tonality or "Major" in tonality:
        return major_scales[note]
    elif "minor" in tonality or "Minor" in tonality:
        return minor_scales[note]
    else:
        raise ValueError(f"Unknown key {full_key}")


def basic_space_representation(chord, diatonic_scale):
    chord = [note % 12 for note in chord]
    a = [chord[0]]
    b = a + [(a[0] + 7) % 12]
    c = sorted(list(set(chord)))
    d = diatonic_scale  # Use the passed diatonic scale
    return {
        'a': a,
        'b': b,
        'c': c,
        'd': d
    }

def circle_of_fifths_shifts(root1, root2):
    d = [0, 2, 4, 5, 7, 9, 11]
    if root1 not in d or root2 not in d:
        # Skip problematic chords
        return float('inf')
    idx1 = d.index(root1)
    idx2 = d.index(root2)
    shifts_right = (idx2 - idx1) % 7
    shifts_left = (idx1 - idx2) % 7
    return min(shifts_right, shifts_left)

def non_common_pitch_classes(chord1, chord2):
    count = 0
    for level in ['a', 'b', 'c', 'd']:
        count += len(set(chord1[level]) - set(chord2[level]))
        count += len(set(chord2[level]) - set(chord1[level]))
    return count / 2

def chord_distance(chord1, chord2):
    j = circle_of_fifths_shifts(chord1['a'][0], chord2['a'][0])
    if j == float('inf'):
        # Skip problematic chords
        return float('inf')
    k = non_common_pitch_classes(chord1, chord2)
    return j + k

def main():
    directory = "/home/dxwoo/Documents/Code_2/MIDIPROCESS/MIDIPROCESS/MUSICAL_SPACE/MS_2_csv"
    output_file = "MS_2_distances.csv"

    results = []

    for file_name in os.listdir(directory):
        if file_name.endswith(".csv"):
            file_path = os.path.join(directory, file_name)
            key, chords_data_dicts = parse_csv(file_path)
            diatonic_scale = get_diatonic_scale(key)

            # Extract and parse the chords from the dictionary rows
            chords_data = [list(map(int, chord_dict["Chords"].split())) for chord_dict in chords_data_dicts]
            
            chords_representation = [basic_space_representation(chord, diatonic_scale) for chord in chords_data]
            distances = []
            for i in range(len(chords_representation) - 1):
                distance = chord_distance(chords_representation[i], chords_representation[i + 1])
                if distance != float('inf'):
                    distances.append(distance)
            if distances:
                avg_distance = sum(distances) / len(distances)
                results.append((file_name, avg_distance))

    # Write results to a new CSV
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['CSV Name', 'Average Distance'])
        for row in results:
            writer.writerow(row)

if __name__ == "__main__":
    main()
