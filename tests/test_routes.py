import pytest
from unittest.mock import patch
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return {"status": "success", "package1_total_services": 5}, 200

    @app.route("/download/csv")
    def download_csv():
        return "id,name\n1,Test Service", 200

    app.config["TESTING"] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert "package1_total_services" in response.json

def test_download_csv(client):
    response = client.get("/download/csv")
    assert response.status_code == 200
    assert "id,name\n1,Test Service" in response.get_data(as_text=True)
