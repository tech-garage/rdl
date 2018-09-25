import json
import pytest
from questions.application import app

@pytest.fixture
def client():
    return app.test_client()

def test_response(client):
    result = client.get()
    response_body = json.loads(result.get_data())
    assert result.status_code == 200

