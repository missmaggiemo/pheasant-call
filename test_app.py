# Tests for the app
import os
import pytest
import json
from providers import providers_app, init_db

TESTDB = 'test.sqlite3'


def dollar_to_float(dollar):
	return float(dollar.replace('$', '').replace(',', ''))


@pytest.fixture
def client():
    providers_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(TESTDB)
    providers_app.config['TESTING'] = True
    client = providers_app.test_client()
    init_db()
    yield client
    os.remove(TESTDB)


def test_index(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'Hello, Bain Challenge!' in rv.data


def test_load_sample_data(client):
    rv = client.get('/load_data?filename=test_data.csv')
    assert b'Finished 10 lines' in rv.data


def test_sample_query_limit(client):
    client.get('/load_data?filename=test_data.csv')
    rv = client.get('/providers?limit=2')
    data = json.loads(rv.data)
    assert len(data) == 2


def test_sample_query_state(client):
    client.get('/load_data?filename=test_data.csv')
    rv = client.get('/providers?state=AL')
    data = json.loads(rv.data)
    assert len(data) == 9
    assert data[0]['Provider State'] == 'AL'


def test_sample_query_max_discharges(client):
    client.get('/load_data?filename=test_data.csv')
    rv = client.get('/providers?max_discharges=100')
    data = json.loads(rv.data)
    assert len(data) == 8
    assert data[0]['Total Discharges'] < 100


def test_sample_query_min_discharges(client):
    client.get('/load_data?filename=test_data.csv')
    rv = client.get('/providers?min_discharges=90')
    data = json.loads(rv.data)
    assert len(data) == 2
    assert data[0]['Total Discharges'] > 90


def test_sample_query_max_average_covered_charges(client):
    client.get('/load_data?filename=test_data.csv')
    rv = client.get('/providers?max_average_covered_charges=32000')
    data = json.loads(rv.data)
    assert len(data) == 6
    assert dollar_to_float(data[0]['Average Covered Charges']) < 32000


def test_sample_query_min_average_covered_charges(client):
    client.get('/load_data?filename=test_data.csv')
    rv = client.get('/providers?min_average_covered_charges=32000')
    data = json.loads(rv.data)
    assert len(data) == 3
    assert dollar_to_float(data[0]['Average Covered Charges']) > 32000


def test_sample_query_max_average_medicare_payments(client):
    client.get('/load_data?filename=test_data.csv')
    rv = client.get('/providers?max_average_medicare_payments=5000')
    data = json.loads(rv.data)
    assert len(data) == 6
    assert dollar_to_float(data[0]['Average Medicare Payments']) < 5000


def test_sample_query_min_average_medicare_payments(client):
    client.get('/load_data?filename=test_data.csv')
    rv = client.get('/providers?min_average_medicare_payments=5000')
    data = json.loads(rv.data)
    assert len(data) == 3
    assert dollar_to_float(data[0]['Average Medicare Payments']) > 5000
