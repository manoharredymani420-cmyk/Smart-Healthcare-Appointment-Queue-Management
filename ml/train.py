import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
from ml.generate_dataset import generate_synthetic_data

def train_and_evaluate():
    ml_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(ml_dir, 'synthetic_queue_data.csv')
    
    if not os.path.exists(csv_path):
        print("Generating synthetic training data...")
        df = generate_synthetic_data()
        df.to_csv(csv_path, index=False)
    else:
        df = pd.read_csv(csv_path)

    feature_cols = [
        'doctor_id', 'department_id', 'day_of_week', 'appointment_hour',
        'patients_ahead', 'queue_length', 'average_consultation_time',
        'appointments_scheduled', 'historical_average_wait'
    ]
    target_col = 'waiting_time_minutes'

    X = df[feature_cols]
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=4, random_state=42)
    }

    best_model_name = None
    best_model = None
    best_r2 = -float('inf')
    results = {}

    print("\n--- ML Waiting Time Model Evaluation ---")
    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        
        mae = mean_absolute_error(y_test, preds)
        rmse = root_mean_squared_error(y_test, preds)
        r2 = r2_score(y_test, preds)
        
        results[name] = {'MAE': mae, 'RMSE': rmse, 'R2': r2}
        print(f"[{name}] MAE: {mae:.2f} min | RMSE: {rmse:.2f} min | R²: {r2:.4f}")

        if r2 > best_r2:
            best_r2 = r2
            best_model_name = name
            best_model = model

    print(f"\nBest Selected Model: {best_model_name} (R² = {best_r2:.4f})")
    
    # Save the best model alongside metadata
    model_artifact = {
        'model': best_model,
        'model_name': best_model_name,
        'feature_cols': feature_cols,
        'version': 'v1.0',
        'metrics': results[best_model_name]
    }
    
    model_path = os.path.join(ml_dir, 'model.joblib')
    joblib.dump(model_artifact, model_path)
    print(f"Saved best model artifact to: {model_path}")
    return model_artifact

if __name__ == '__main__':
    train_and_evaluate()
