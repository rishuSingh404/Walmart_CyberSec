import random
try:
    from .models import BehavioralData
except ImportError:
    from models import BehavioralData

def analyze_user_behavior(user, new_fingerprint_data):
    """
    Analyzes user behavior against their stored fingerprints.

    In a real implementation, this would involve:
    1. Retrieving all historical fingerprints for the user.
    2. Using a sophisticated algorithm (e.g., DTW, HMM, or a neural network)
       to compare the new fingerprint with the historical average or model.
    3. Calculating a deviation score (anomaly_score).
    4. Determining if the deviation is significant enough to be an anomaly.
    """

    # For now, we use a mock implementation.
    # We retrieve the last fingerprint to simulate a check, but the logic is random.
    last_fingerprint = BehavioralData.query.filter_by(user_id=user.id).order_by(BehavioralData.created_at.desc()).first()

    if not last_fingerprint:
        # No historical data, cannot determine anomaly yet.
        return {
            "is_anomaly": False,
            "anomaly_score": 0.05,
            "confidence": 0.5,
            "anomalous_fields": []
        }

    # Mocked analysis logic
    is_anomaly = random.random() < 0.1  # 10% chance of anomaly
    anomaly_score = round(random.uniform(0.05, 0.4 if not is_anomaly else 0.8), 2)
    confidence = round(random.uniform(0.75, 0.95), 2)
    
    anomalous_fields = []
    if is_anomaly:
        # Randomly pick some fields that are "anomalous" from the input data
        possible_fields = list(new_fingerprint_data.keys())
        if possible_fields:
            anomalous_fields = random.sample(possible_fields, k=min(len(possible_fields), 2))

    return {
        "is_anomaly": is_anomaly,
        "anomaly_score": anomaly_score,
        "confidence": confidence,
        "anomalous_fields": anomalous_fields
    } 