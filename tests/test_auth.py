def test_health_check(client):
    res = client.get('/api/health')
    assert res.status_code == 200
    json_data = res.get_json()
    assert json_data['success'] is True
    assert json_data['data']['status'] == 'healthy'

def test_register_patient_success(client):
    payload = {
        'name': 'New Patient',
        'email': 'newpatient@example.com',
        'password': 'Password123!',
        'role': 'patient',
        'phone': '555-9876'
    }
    res = client.post('/api/auth/register', json=payload)
    assert res.status_code == 201
    json_data = res.get_json()
    assert json_data['success'] is True
    assert 'access_token' in json_data['data']
    assert json_data['data']['user']['email'] == 'newpatient@example.com'

def test_register_duplicate_email(client):
    payload = {
        'name': 'Duplicate',
        'email': 'patient@test.com',
        'password': 'Password123!'
    }
    res = client.post('/api/auth/register', json=payload)
    assert res.status_code == 409
    json_data = res.get_json()
    assert json_data['success'] is False
    assert json_data['error']['code'] == 'EMAIL_ALREADY_EXISTS'

def test_login_success(client):
    payload = {
        'email': 'patient@test.com',
        'password': 'Pass123!'
    }
    res = client.post('/api/auth/login', json=payload)
    assert res.status_code == 200
    json_data = res.get_json()
    assert json_data['success'] is True
    assert 'access_token' in json_data['data']

def test_login_invalid_password(client):
    payload = {
        'email': 'patient@test.com',
        'password': 'WrongPassword'
    }
    res = client.post('/api/auth/login', json=payload)
    assert res.status_code == 401
    json_data = res.get_json()
    assert json_data['success'] is False
    assert json_data['error']['code'] == 'INVALID_CREDENTIALS'

def test_me_protected_endpoint(client, patient_token):
    headers = {'Authorization': f'Bearer {patient_token}'}
    res = client.get('/api/auth/me', headers=headers)
    assert res.status_code == 200
    json_data = res.get_json()
    assert json_data['success'] is True
    assert json_data['data']['email'] == 'patient@test.com'
