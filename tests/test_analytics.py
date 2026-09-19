def test_analytics_overview(client):
    res = client.get('/api/analytics/overview')
    assert res.status_code == 200
    json_data = res.get_json()
    assert json_data['success'] is True
    data = json_data['data']
    assert 'total_appointments' in data
    assert 'active_in_queue' in data

def test_analytics_departments(client):
    res = client.get('/api/analytics/departments')
    assert res.status_code == 200
    json_data = res.get_json()
    assert json_data['success'] is True
    assert isinstance(json_data['data'], list)
