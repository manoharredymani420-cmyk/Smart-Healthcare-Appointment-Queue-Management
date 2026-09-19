import os
import numpy as np
import pandas as pd

def generate_synthetic_data(num_samples=2500, random_seed=42):
    np.random.seed(random_seed)

    doctor_ids = np.random.randint(1, 11, size=num_samples)
    department_ids = np.random.randint(1, 6, size=num_samples)
    day_of_week = np.random.randint(0, 7, size=num_samples)
    appointment_hour = np.random.randint(8, 18, size=num_samples)
    patients_ahead = np.random.randint(0, 15, size=num_samples)
    
    # Queue length is at least patients_ahead + upcoming/in-progress (0 to 5)
    queue_length = patients_ahead + np.random.randint(1, 6, size=num_samples)
    
    # Department base consultation duration: 1: General (10m), 2: Peds (15m), 3: Derm (12m), 4: Ortho (18m), 5: Cardio (20m)
    dept_base_times = {1: 10.0, 2: 15.0, 3: 12.0, 4: 18.0, 5: 20.0}
    avg_consultation_time = np.array([dept_base_times.get(d, 15.0) for d in department_ids])
    # Add doctor personal speed variation (+/- 2 minutes)
    avg_consultation_time += np.random.uniform(-2.0, 2.0, size=num_samples)
    avg_consultation_time = np.clip(avg_consultation_time, 5.0, 35.0)

    appointments_scheduled = np.random.randint(10, 35, size=num_samples)
    historical_average_wait = (patients_ahead * avg_consultation_time * 0.85) + np.random.normal(0, 3, size=num_samples)
    historical_average_wait = np.clip(historical_average_wait, 0, None)

    # Hour rush factor: morning (10-12) and evening (16-17) are busier
    hour_factor = np.where((appointment_hour >= 10) & (appointment_hour <= 12), 1.15,
                  np.where((appointment_hour >= 16) & (appointment_hour <= 17), 1.10, 1.0))

    # Day of week factor: Mondays (0) and Fridays (4) are busier
    day_factor = np.where((day_of_week == 0) | (day_of_week == 4), 1.10, 1.0)

    # Realistic waiting time target
    noise = np.random.normal(0, 4.0, size=num_samples)
    waiting_time = (patients_ahead * avg_consultation_time * hour_factor * day_factor) + (queue_length * 0.5) + noise
    waiting_time = np.clip(waiting_time, 0.0, 180.0)

    df = pd.DataFrame({
        'doctor_id': doctor_ids,
        'department_id': department_ids,
        'day_of_week': day_of_week,
        'appointment_hour': appointment_hour,
        'patients_ahead': patients_ahead,
        'queue_length': queue_length,
        'average_consultation_time': np.round(avg_consultation_time, 1),
        'appointments_scheduled': appointments_scheduled,
        'historical_average_wait': np.round(historical_average_wait, 1),
        'waiting_time_minutes': np.round(waiting_time, 1)
    })

    return df

if __name__ == '__main__':
    ml_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(ml_dir, 'synthetic_queue_data.csv')
    df = generate_synthetic_data()
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} synthetic queue samples at {output_path}")
