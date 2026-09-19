from datetime import date

def test_queue_flow(client, patient_token, doctor_token):
    p_headers = {'Authorization': f'Bearer {patient_token}'}
    d_headers = {'Authorization': f'Bearer {doctor_token}'}
    today_str = date.today().isoformat()

    # Book appointment
    payload = {
        'doctor_id': 1,
        'appointment_date': today_str,
        'appointment_time': '09:30',
        'reason': 'Queue Test'
    }
    b_res = client.post('/api/appointments', json=payload, headers=p_headers)
    assert b_res.status_code == 201
    appt_id = b_res.get_json()['data']['id']

    # Get Queue record
    q_res = client.get(f'/api/queue/{appt_id}')
    assert q_res.status_code == 200
    q_data = q_res.get_json()['data']
    assert q_data['queue_position'] >= 1
    assert q_data['queue_status'] == 'WAITING'

    # Doctor calls next
    call_res = client.post('/api/queue/doctor/1/next', headers=d_headers)
    assert call_res.status_code == 200
