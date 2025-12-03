from pynput import mouse
import time
import csv
import os

# 1. SETUP
# We will save data to a 'data' folder
if not os.path.exists('data'):
    os.makedirs('data')

FILE_NAME = "data/mouse_log.csv"

# 2. PREPARE THE FILE
# If the file doesn't exist, create it and add headers
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "event_type", "x", "y"])

print(f"🔴 RECORDING STARTED. Data is being saved to {FILE_NAME}")
print("Move your mouse naturally. Press the STOP button in PyCharm to finish.")

def log_data(event_type, x, y):
    """Saves a single mouse event to the CSV file"""
    with open(FILE_NAME, mode='a', newline='') as f:
        writer = csv.writer(f)
        # We record the current time, what happened, and where
        writer.writerow([time.time(), event_type, x, y])

# 3. DEFINE LISTENERS
def on_move(x, y):
    # Log movement (we only log every few moves to avoid flooding data, optional)
    log_data("move", x, y)

def on_click(x, y, button, pressed):
    # Log clicks
    action = "click_pressed" if pressed else "click_released"
    log_data(action, x, y)

# 4. START LISTENING
# This loop keeps running until you stop the script manually
with mouse.Listener(on_move=on_move, on_click=on_click) as listener:
    listener.join()