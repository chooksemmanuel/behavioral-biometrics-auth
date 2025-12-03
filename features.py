import pandas as pd
import numpy as np
import os


def calculate_features(input_file, output_file):
    print(f"Reading data from {input_file}...")

    # 1. Load the raw data
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print("Error: mouse_log.csv not found. Did you run recorder.py?")
        return

    # Filter only for 'move' events (we focus on movement physics)
    df = df[df['event_type'] == 'move'].copy()

    # 2. Calculate Differences (Delta)
    # How much did X, Y, and Time change since the last recorded point?
    df['dx'] = df['x'].diff()
    df['dy'] = df['y'].diff()
    df['dt'] = df['timestamp'].diff()

    # Remove the first row (it has NaN because there's no previous point)
    df = df.dropna()
    # Remove rows where time difference is 0 (to avoid division by zero errors)
    df = df[df['dt'] > 0]

    # 3. Calculate Physics Features
    # Velocity (Distance / Time)
    df['velocity_x'] = df['dx'] / df['dt']
    df['velocity_y'] = df['dy'] / df['dt']
    df['speed'] = np.sqrt(df['velocity_x'] ** 2 + df['velocity_y'] ** 2)

    # Acceleration (Change in Velocity / Time)
    df['acc_x'] = df['velocity_x'].diff() / df['dt']
    df['acc_y'] = df['velocity_y'].diff() / df['dt']
    df['acceleration'] = np.sqrt(df['acc_x'] ** 2 + df['acc_y'] ** 2)

    # Angle (Direction of movement in radians)
    df['angle'] = np.arctan2(df['dy'], df['dx'])

    # Angular Velocity (How fast the angle changes - measures "curvature")
    df['angular_velocity'] = df['angle'].diff() / df['dt']

    # 4. Clean up
    # Drop any new NaNs created by the diff() operations
    features = df.dropna()

    # Select only the math columns for the AI
    final_features = features[['speed', 'acceleration', 'angular_velocity']]

    # 5. Save
    final_features.to_csv(output_file, index=False)
    print(f"✅ Success! Extracted {len(final_features)} movement patterns.")
    print(f"Features saved to: {output_file}")


# --- Execution ---
if __name__ == "__main__":
    calculate_features('data/mouse_log.csv', 'data/features.csv')