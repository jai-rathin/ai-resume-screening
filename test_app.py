import pytest
from app import app

@pytest.fixture
def client():
    """A test client for the app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test that the home page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"AI Resume Screener" in response.data

def test_screen_no_data(client):
    """Test that submitting the form with no data returns an error."""
    response = client.post('/screen', data={})
    assert response.status_code == 200
    # Should display the missing job description error
    assert b"Please enter a job description" in response.data
#testing230
#testing100
#testing300
