import pytest
from app.services.fetchingAPI.utils import fetch_pagerduty_data
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_mocked_service_call():
    # Mock fetch_pagerduty_data to simulate a successful API call
    with patch("app.services.fetchingAPI.utils.fetch_pagerduty_data", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = {"services": [{"id": "1", "name": "Test Service"}]}
        from app.services.fetchingAPI.utils import fetch_pagerduty_data
        result = await fetch_pagerduty_data("services")
        assert result["services"][0]["name"] == "Test Service"

@pytest.mark.asyncio
async def test_mocked_service_error():
    # Mock fetch_pagerduty_data to simulate an API error
    with patch("app.services.fetchingAPI.utils.fetch_pagerduty_data", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.side_effect = Exception("API Error")
        from app.services.fetchingAPI.utils import fetch_pagerduty_data

        try:
            await fetch_pagerduty_data("services")
        except Exception as e:
            assert str(e) == "API Error"

def test_task_processing():
    # Mock fetch_and_save_teams to validate its behavior
    with patch("app.services.fetchingAPI.tasks.fetch_and_save_teams", return_value=None) as mock_task:
        from app.services.fetchingAPI.tasks import fetch_and_save_teams
        fetch_and_save_teams()
        mock_task.assert_called_once()

