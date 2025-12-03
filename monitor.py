import time
import pandas as pd
import numpy as np
import joblib
import ctypes
from pynput import mouse
from collections import deque

# --- CONFIGURATION ---
TEST_MODE = True  # Set to False to ACTUALLY lock the screen
ANOMALY_THRESHOLD = 15  # How many "bad moves" before locking?
WINDOW_SIZE = 20  # How many mouse events to analyze at once

# Load the Brain
print("Loading User Profile...")
try:
    clf = joblib.load('models/user_profile.pkl')
    print("✅ Profile Loaded. System Armed.")
except FileNotFoundError:
    print("❌ Error: user_profile.pkl not found.")
    exit()

# Buffer to store live mouse data
event_buffer = deque(maxlen=WINDOW_SIZE)
anomaly_counter = 0


def lock_station():
    """Locks the Windows Workstation"""
    print("!!! INTRUDER DETECTED - LOCKING SYSTEM !!!")
    if not TEST_MODE:
        ctypes.windll.user32.LockWorkStation()


def get_live_features(buffer):
    """Calculates physics from the live buffer (Same math as features.py)"""
    df = pd.DataFrame(list(buffer), columns=['timestamp', 'event_type', 'x', 'y'])

    # Filter for moves
    df = df[df['event_type'] == 'move'].copy()
    if len(df) < 2: return None

    # Calculate Physics
    df['dx'] = df['x'].diff()
    df['dy'] = df['y'].diff()
    df['dt'] = df['timestamp'].diff()
    df = df.dropna()
    df = df[df['dt'] > 0]  # Avoid divide by zero

    if len(df) == 0: return None

    df['velocity_x'] = df['dx'] / df['dt']
    df['velocity_y'] = df['dy'] / df['dt']
    df['speed'] = np.sqrt(df['velocity_x'] ** 2 + df['velocity_y'] ** 2)

    df['acc_x'] = df['velocity_x'].diff() / df['dt']
    df['acc_y'] = df['velocity_y'].diff() / df['dt']
    df['acceleration'] = np.sqrt(df['acc_x'] ** 2 + df['acc_y'] ** 2)

    df['angle'] = np.arctan2(df['dy'], df['dx'])
    df['angular_velocity'] = df['angle'].diff() / df['dt']

    # Return the average behavior of this window
    # We take the mean of the features to get a "snapshot" of current behavior
    latest_features = df[['speed', 'acceleration', 'angular_velocity']].mean().to_frame().T

    # Fill NaNs if any (can happen with small windows)
    latest_features = latest_features.fillna(0)
    return latest_features


def on_move(x, y):
    global anomaly_counter

    # Add data to buffer
    event_buffer.append([time.time(), 'move', x, y])

    # Only check if buffer is full
    if len(event_buffer) == WINDOW_SIZE:
        features = get_live_features(event_buffer)

        if features is not None:
            # PREDICT: 1 = User, -1 = Anomaly
            prediction = clf.predict(features)[0]

            if prediction == -1:
                anomaly_counter += 1
                print(f"⚠️ Suspicious Activity detected! (Level: {anomaly_counter}/{ANOMALY_THRESHOLD})")
            else:
                # If behavior returns to normal, slowly lower the alert level
                if anomaly_counter > 0:
                    anomaly_counter -= 1
                    print(f"✅ User verified. Alert level dropping ({anomaly_counter})")

            # TRIGGER LOCK
            if anomaly_counter >= ANOMALY_THRESHOLD:
                lock_station()
                anomaly_counter = 0  # Reset after locking
                # Optional: Quit script after lock so you can log back in peacefully
                # return False


# Start Listening
print("🟢 MONITORING STARTED... (Move mouse to test)")
with mouse.Listener(on_move=on_move) as listener:
    listener.join()