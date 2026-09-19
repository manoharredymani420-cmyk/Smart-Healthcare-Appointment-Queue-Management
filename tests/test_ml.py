def test_ml_prediction_endpoint(client):
    payload = {
        'doctor_id': 1,
        'department_id': 1,
        'day_of_week': 2,
        'appointment_hour': 10,
        'patients_ahead': 4,
        'queue_length': 6,
        'average_consultation_time': 15.0
    }
    res = client.post('/api/predictions/waiting-time', json=payload)
    assert res.status_code == 200
    json_data = res.get_json()
    assert json_data['success'] is True
    assert 'estimated_wait_minutes' in json_data['data']
    assert json_data['data']['estimated_wait_minutes'] > 0

def test_ml_zero_patients_ahead(client):
    payload = {
        'doctor_id': 1,
        'patients_ahead': 0
    }
    res = client.post('/api/predictions/waiting-time', json=payload)
    assert res.status_code == 200
    json_data = res.get_json()
    assert json_data['data']['estimated_wait_minutes'] == 0
