import joblib
import os
import pandas as pd
import warnings

# Suppress scikit-learn version warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

# Get the absolute path to the model directory
# This assumes the script is run from the root of the project where 'backend' and 'model' are siblings
MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model'))

RISK_MODEL_PATH = os.path.join(MODEL_DIR, 'risk_model.joblib')
SCALER_PATH = os.path.join(MODEL_DIR, 'risk_scaler.joblib')
LABEL_ENCODER_PATH = os.path.join(MODEL_DIR, 'risk_label_encoder.joblib')

class RiskModel:
    def __init__(self, model_path=RISK_MODEL_PATH, scaler_path=SCALER_PATH, encoder_path=LABEL_ENCODER_PATH):
        try:
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            self.encoder = joblib.load(encoder_path)
            print(f"Model loaded successfully from {model_path}")
        except FileNotFoundError as e:
            print(f"Error loading model files: {e}")
            print("Please ensure the model files are present in the 'model' directory.")
            self.model = None
            self.scaler = None
            self.encoder = None
        except Exception as e:
            print(f"Unexpected error loading model: {e}")
            self.model = None
            self.scaler = None
            self.encoder = None

    def predict(self, data):
        if not all([self.model, self.scaler, self.encoder]):
            # Return a default/mock prediction if models are not loaded
            print("Models not loaded, returning mock prediction")
            return {"risk_label": "low", "score": 0.2}

        try:
            # Prepare the dataframe for prediction
            df = pd.DataFrame([data])
            
            # Feature engineering from timestamp (example: hour of day)
            try:
                if 'timestamp' in df.columns:
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                    df['hour'] = df['timestamp'].dt.hour
                    df = df.drop(columns=['timestamp'])
                else:
                    df['hour'] = 12
            except Exception as e:
                print(f"Timestamp processing error: {e}")
                df['hour'] = 12
                if 'timestamp' in df.columns:
                    df = df.drop(columns=['timestamp'])

            # Get the expected feature names from the scaler
            if not hasattr(self.scaler, 'feature_names_in_'):
                print("Scaler doesn't have feature_names_in_ attribute, using default features")
                model_features = ['typing_speed', 'mouse_distance', 'click_count', 'session_duration', 'scroll_depth', 'ip_location_score', 'device_type_score', 'hour']
            else:
                model_features = list(self.scaler.feature_names_in_)

            # Add missing columns with default values
            for col in model_features:
                if col not in df.columns:
                    df[col] = 0
            
            # Ensure we have all required columns in the correct order
            df = df[model_features]

            # Scale the features
            df_scaled = self.scaler.transform(df)

            # Make prediction
            prediction_encoded = self.model.predict(df_scaled)
            prediction_proba = self.model.predict_proba(df_scaled)
            
            # Decode the label
            risk_label = self.encoder.inverse_transform(prediction_encoded)[0]
            
            # Get the score for the predicted class
            score = prediction_proba[0][prediction_encoded[0]]

            return {"risk_label": risk_label, "score": float(score)}

        except Exception as e:
            print(f"Prediction error: {e}")
            # Return a safe fallback
            return {"risk_label": "low", "score": 0.2}

# Initialize a single instance of the model to be used by the app
risk_model_instance = RiskModel() 