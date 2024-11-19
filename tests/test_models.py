import pytest
import json
import os
from app.models import Service, Team

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_JSON_DIR = os.path.join(BASE_DIR, "../app/static/json")

@pytest.fixture
def mock_services():
    with open(os.path.join(STATIC_JSON_DIR, "mock_services.json"), "r") as f:
        return json.load(f)

@pytest.fixture
def mock_teams():
    with open(os.path.join(STATIC_JSON_DIR, "mock_teams.json"), "r") as f:
        return json.load(f)

@pytest.mark.parametrize("missing_field", ["name", "id"])
def test_service_creation_missing_fields(mock_services, missing_field):
    service_data = mock_services["services"][0]
    service_data.pop(missing_field, None)

    with pytest.raises(TypeError):  # Adjust for the actual exception type raised by your code
        Service(**service_data)

def test_service_relationships(mock_services, mock_teams):
    service_data = mock_services["services"][0]
    team_data = mock_teams["teams"][0]

    service = Service(id=service_data["id"], name=service_data["name"])
    team = Team(id=team_data["id"], name=team_data["name"])
    service.teams.append(team)

    assert len(service.teams) == 1
    assert service.teams[0].id == team.id
    assert len(team.services) == 1
    assert team.services[0].id == service.id
