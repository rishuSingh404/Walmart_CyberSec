import pandas as pd
import numpy as np
import joblib
import optuna
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Set random seed for reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

def preprocess_data(df):
    """Preprocess the dataset for model training"""
    # Create a copy to avoid modifying the original
    df_processed = df.copy()
    
    # Extract hour from timestamp
    df_processed['hour'] = df_processed['timestamp'].apply(lambda x: int(x.split(':')[0]))
    
    # Convert risk_label to integer classes
    label_encoder = LabelEncoder()
    df_processed['risk_label_encoded'] = label_encoder.fit_transform(df_processed['risk_label'])
    
    # Save the label encoder for later use
    joblib.dump(label_encoder, 'risk_label_encoder.joblib')
    
    # Define features and target
    features = [
        'typing_speed', 'mouse_distance', 'click_count', 
        'session_duration', 'scroll_depth', 'ip_location_score',
        'device_type_score', 'hour'
    ]
    
    X = df_processed[features]
    y = df_processed['risk_label_encoded']
    
    # Scale numerical features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Save the scaler for inference
    joblib.dump(scaler, 'risk_scaler.joblib')
    
    return X_scaled, y, features, label_encoder

def visualize_results(model, X_test, y_test, label_encoder):
    """Visualize the model results"""
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Create a confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    class_names = label_encoder.classes_
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    plt.savefig('confusion_matrix.png')
    
    # Feature importance
    feature_importances = model.feature_importances_
    feature_names = [
        'typing_speed', 'mouse_distance', 'click_count', 
        'session_duration', 'scroll_depth', 'ip_location_score',
        'device_type_score', 'hour'
    ]
    
    plt.figure(figsize=(10, 8))
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': feature_importances
    }).sort_values('importance', ascending=False)
    
    sns.barplot(x='importance', y='feature', data=importance_df)
    plt.title('Feature Importance')
    plt.savefig('feature_importance.png')
    
def objective(trial):
    """Optuna objective function for hyperparameter tuning"""
    # Define the hyperparameters to optimize
    n_estimators = trial.suggest_int('n_estimators', 50, 300)
    max_depth = trial.suggest_int('max_depth', 5, 30)
    min_samples_split = trial.suggest_int('min_samples_split', 2, 20)
    min_samples_leaf = trial.suggest_int('min_samples_leaf', 1, 10)
    max_features = trial.suggest_categorical('max_features', ['sqrt', 'log2', None])
    
    # Create the model with the suggested hyperparameters
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        max_features=max_features,
        random_state=RANDOM_SEED
    )
    
    # Perform cross-validation
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
    
    # Return the mean accuracy
    return scores.mean()

def train_model():
    """Main function to load data and train the model"""
    print("Loading and preprocessing data...")
    df = pd.read_csv('dataset.csv')
    
    print("\nDataset shape:", df.shape)
    print("\nData overview:")
    print(df.head())
    
    # Check for missing values
    print("\nMissing values:")
    print(df.isnull().sum())
    
    # Basic statistics
    print("\nBasic statistics:")
    print(df.describe())
    
    # Target distribution
    print("\nTarget distribution:")
    print(df['risk_label'].value_counts())
    
    # Preprocess data
    X, y, features, label_encoder = preprocess_data(df)
    
    # Split data into train and test sets
    global X_train, X_test, y_train, y_test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_SEED, stratify=y)
    
    print("\nStarting hyperparameter optimization with Optuna...")
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=50)
    
    best_params = study.best_params
    print("\nBest hyperparameters:", best_params)
    
    # Train the model with the best parameters
    best_model = RandomForestClassifier(
        n_estimators=best_params['n_estimators'],
        max_depth=best_params['max_depth'],
        min_samples_split=best_params['min_samples_split'],
        min_samples_leaf=best_params['min_samples_leaf'],
        max_features=best_params['max_features'],
        random_state=RANDOM_SEED
    )
    
    print("\nTraining final model with best parameters...")
    best_model.fit(X_train, y_train)
    
    # Evaluate on test set
    y_pred = best_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nTest accuracy: {accuracy:.4f}")
    
    # Detailed classification report
    print("\nClassification report:")
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))
    
    # Visualize results
    visualize_results(best_model, X_test, y_test, label_encoder)
    
    # Save the model
    print("\nSaving the model...")
    joblib.dump(best_model, 'risk_model.joblib')
    
    print("\nTraining completed successfully!")
    return best_model

if __name__ == "__main__":
    train_model() 