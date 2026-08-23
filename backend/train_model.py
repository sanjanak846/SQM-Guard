from app.services.anomaly_scorer import train_model


if __name__ == "__main__":
    train_model("../security logs.csv")