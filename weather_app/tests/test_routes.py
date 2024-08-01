import pytest
from app import app, db
from app.models import CitySearch


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client
        db.drop_all()


def test_index(client):
    rv = client.get('/')
    assert b'Weather App' in rv.data


def test_weather_search(client):
    rv = client.post('/', data=dict(city='London'), follow_redirects=True)
    assert b'Weather in London' in rv.data


def test_history_api(client):
    client.post('/', data=dict(city='London'), follow_redirects=True)
    rv = client.get('/api/history')
    assert b'London' in rv.data


