import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib  # This saves the model to a file
import os


def train_user_model(data_path, model_path):
    print("Loading feature data...")

    # 1. Load the physics data we just calculated
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print("Error: features.csv not found. Run features.py first.")
        return

    # 2. Initialize the Algorithm
    # contamination=0.01 means we assume 1% of your own data might be "noise" (accidental slips)
    # random_state=42 ensures we get the same result every time we train
    clf = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)

    print(f"Training Isolation Forest on {len(df)} patterns...")

    # 3. Train the model (Fit)
    # The model looks at Speed, Acceleration, and Angular Velocity
    clf.fit(df)

    # 4. Save the "Brain"
    # We save it so the monitor script can use it later without retraining
    if not os.path.exists('models'):
        os.makedirs('models')

    joblib.dump(clf, model_path)
    print(f"✅ Success! Model saved to: {model_path}")
    print("The system now knows your biometric signature.")


# --- Execution ---
if __name__ == "__main__":
    train_user_model('data/features.csv', 'models/user_profile.pkl')