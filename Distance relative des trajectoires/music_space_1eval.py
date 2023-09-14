import os
import csv
import numpy as np
from scipy.optimize import curve_fit
from numpy.polynomial import Polynomial


def polynomial_func(x, *coeffs):
    """ Polynomial function for curve fitting """
    p = Polynomial(coeffs)
    return p(x)

def get_data_from_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header
        raw_data = list(reader)
        data = [[float(row[0]), float(row[1]), float(row[2]), float(row[3])] for row in raw_data]
    
    # Apply the transformation to replace chord notes with fundamental note
    processed_data = replace_with_fundamental(data)
    return processed_data

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

def compute_avg_trajectory(data_dicts, degree=2):
    times = []
    pitches = []

    # Aggregate all times and pitches from the data
    for key, data in data_dicts.items():
        for time, pitch in data.items():
            times.append(time)
            pitches.append(pitch)

    # If there are no times or pitches, return an empty trajectory
    if not times or not pitches:
        return []

    # Fit a polynomial model to the aggregated data
    coeffs, _ = curve_fit(polynomial_func, times, pitches, p0=[0]*(degree+1))
    
    avg_trajectory = [(time, polynomial_func(time, *coeffs)) for time in set(times)]
    return sorted(avg_trajectory, key=lambda x: x[0])

def fit_to_avg(data, avg_trajectory, degree=3):
    common_times = [point[0] for point in data if point[0] in dict(avg_trajectory)]
    if not common_times:
        return float('inf')
    
    x_data = common_times
    y_data = [dict(data)[time] for time in common_times]
    y_avg = [dict(avg_trajectory)[time] for time in common_times]

    popt, _ = curve_fit(polynomial_func, y_data, y_avg, p0=[0]*(degree+1))
    
    residuals = [y - polynomial_func(x, *popt) for x, y in zip(y_data, y_avg)]
    distance = np.sqrt(sum([r**2 for r in residuals]))
    
    return distance

def main():
    directory = 'MS_1_csv'
    data_dicts = {}

    for csv_file in os.listdir(directory):
        if csv_file.endswith('.csv'):
            data = get_data_from_csv(os.path.join(directory, csv_file))
            data_dicts[csv_file] = {point[0]: point[1] for point in data}

    avg_trajectory = compute_avg_trajectory(data_dicts)
    # print(data_dicts)

    distances = {}
    for key, data in data_dicts.items():
        distances[key] = fit_to_avg(list(data.items()), avg_trajectory)

    # Files with most deviation
    top_5_files = sorted(distances, key=distances.get, reverse=True)[:5]
    print("Top 5 files with most deviation:")
    for file in top_5_files:
        print(f"{file}: Distance = {distances[file]}")

    # Files with least deviation
    bottom_5_files = sorted(distances, key=distances.get)[:5]
    print("\nTop 5 files with least deviation:")
    for file in bottom_5_files:
        print(f"{file}: Distance = {distances[file]}")

if __name__ == "__main__":
    main()
