from datetime import datetime, date, timedelta

def test_get_doctor_availability(client):
    # Upcoming weekday (e.g. Next Monday)
    today = date.today()
    days_ahead = (0 - today.weekday()) % 7
    if days_ahead == 0:
        days_ahead = 7
    next_monday = today + timedelta(days=days_ahead)

    res = client.get(f'/api/doctors/1/availability?date={next_monday.isoformat()}')
    assert res.status_code == 200
    json_data = res.get_json()
    assert json_data['success'] is True
    assert len(json_data['data']['available_slots']) > 0
    assert '09:00' in json_data['data']['available_slots']

def test_book_appointment_success(client, patient_token):
    headers = {'Authorization': f'Bearer {patient_token}'}
    payload = {
        'doctor_id': 1,
        'appointment_date': '2026-10-05',
        'appointment_time': '10:00',
        'reason': 'Health checkup'
    }
    res = client.post('/api/appointments', json=payload, headers=headers)
    assert res.status_code == 201
    json_data = res.get_json()
    assert json_data['success'] is True
    assert json_data['data']['status'] == 'BOOKED'
    assert json_data['data']['token_number'].startswith('T-01-')

def test_book_duplicate_appointment_conflict(client, patient_token):
    headers = {'Authorization': f'Bearer {patient_token}'}
    payload = {
        'doctor_id': 1,
        'appointment_date': '2026-10-06',
        'appointment_time': '11:00',
        'reason': 'Checkup 1'
    }
    # First booking succeeds
    res1 = client.post('/api/appointments', json=payload, headers=headers)
    assert res1.status_code == 201

    # Second booking for same doctor, date and time must fail with 409 APPOINTMENT_CONFLICT
    res2 = client.post('/api/appointments', json=payload, headers=headers)
    assert res2.status_code == 409
    json_data = res2.get_json()
    assert json_data['success'] is False
    assert json_data['error']['code'] == 'APPOINTMENT_CONFLICT'

def test_cancel_appointment(client, patient_token):
    headers = {'Authorization': f'Bearer {patient_token}'}
    payload = {
        'doctor_id': 1,
        'appointment_date': '2026-10-07',
        'appointment_time': '14:00',
        'reason': 'To be cancelled'
    }
    res = client.post('/api/appointments', json=payload, headers=headers)
    appt_id = res.get_json()['data']['id']

    # Cancel
    del_res = client.delete(f'/api/appointments/{appt_id}', headers=headers)
    assert del_res.status_code == 200
    assert del_res.get_json()['data']['status'] == 'CANCELLED'
