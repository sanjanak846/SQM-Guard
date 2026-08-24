from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest


# Features selected from the SQM-Guard security log dataset
FEATURE_COLUMNS = [
    "EventID",
    "Level",
    "Opcode",
    "Task",
    "Version",
    "ProcessID",
]


MODEL_PATH = Path(__file__).resolve().parent / "anomaly_model.pkl"


def extract_features(log_entry: dict) -> list:
    """
    Convert one security log entry into numeric features
    that the Isolation Forest model can understand.
    """

    features = []

    for column in FEATURE_COLUMNS:
        value = log_entry.get(column, 0)

        try:
            value = float(value)
        except (TypeError, ValueError):
            value = 0.0

        features.append(value)

    return features


def load_training_data(csv_path: str) -> pd.DataFrame:
    """
    Load the SQM-Guard security log dataset.
    """

    df = pd.read_csv(csv_path)

    return df


def train_model(csv_path: str):
    """
    Train the Isolation Forest anomaly detection model.
    """

    df = load_training_data(csv_path)

    # Select the features used by the model
    X = df[FEATURE_COLUMNS].apply(
        pd.to_numeric,
        errors="coerce"
    )

    # Replace missing values with 0
    X = X.fillna(0)

    model = IsolationForest(
        n_estimators=100,
        contamination=0.10,
        random_state=42
    )

    model.fit(X)

    # Save trained model
    joblib.dump(model, MODEL_PATH)

    print("Model trained successfully.")
    print(f"Model saved to: {MODEL_PATH}")

    return model


def score_alert(log_entry: dict) -> dict:
    """
    Calculate anomaly score for one security alert.
    """

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Anomaly model has not been trained yet."
        )

    model = joblib.load(MODEL_PATH)

    features = [extract_features(log_entry)]

    raw_score = model.decision_function(features)[0]

    prediction = model.predict(features)[0]

    # Convert model score into an easy-to-understand risk score
    risk_score = max(
        0,
        min(
            100,
            round((1 - raw_score) * 50, 2)
        )
    )

    return {
       "is_anomaly": bool(prediction == -1),
       "raw_score": float(raw_score),
       "risk_score": float(risk_score),
    }