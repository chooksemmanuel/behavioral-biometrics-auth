## Zero-Trust Behavioral Biometrics

Continuous Authentication System

Status: Completed  
Tech Stack: Python, Scikit-Learn (Isolation Forest), Pandas, Pynput  

## Project Overview
Traditional passwords and MFA only verify identity at the "login" stage. If a user walks away, the session is vulnerable. This project implements "Continuous Authentication" by analyzing the unique "micro-movements" of a user's mouse behavior (velocity, jitter, curvature) to create a digital fingerprint.

## Solution Architecture
## Data Collection: Captures raw X/Y coordinates and timestamp telemetry.
## Feature Engineering: Calculates physics-based features (Acceleration, Angular Velocity).
## Anomaly Detection: Uses an "Isolation Forest" algorithm to learn the legitimate user's pattern.
## Active Defense: Locks the workstation automatically if the anomaly score breaches the threshold.


## System Demonstration

## 1. Feature Engineering Code
The system does not just look at "where" the mouse is, but "how" it moves.

<img width="1919" height="1078" alt="Screenshot 2025-11-26 121104" src="https://github.com/user-attachments/assets/b9326470-a7c0-493f-a1bf-46d6f0728b8f" />


*Figure 1: Python implementation of kinematic feature extraction (Velocity, Acceleration, Jerk) to turn raw logs into behavioral data.*


## 2. Intruder Detection (Live Console)
The system monitors in the background. Below is a log showing the transition from a "Verified User" to an "Intruder" taking control.

<img width="1919" height="1079" alt="Screenshot 2025-11-26 122520" src="https://github.com/user-attachments/assets/22cc1140-18fa-4248-8660-2606f303ad2b" />

*Figure 2: The active monitor flagging anomalous behavior and triggering the system lock mechanism.*


### 3. The Data Structure
Sample of the raw telemetry collected during the training phase.

<img width="1919" height="1079" alt="Screenshot 2025-11-26 115913" src="https://github.com/user-attachments/assets/bcdf27f5-ab2f-4c5a-ab96-56d9d28c0b15" />

*Figure 3: Raw telemetry logs prior to feature extraction.


Usage
1. Record User Data: Run `recorder.py` for 60 seconds to capture your baseline.
2. Train Model: Run `train_model.py` to generate the `user_profile.pkl`.
3. Start Monitoring: Run `monitor.py`. The system will now protect the session.
