# utils.py
import aiohttp
import os

PAGERDUTY_BASE_URL = os.getenv('PAGERDUTY_BASE_URL')

async def fetch_pagerduty_data(endpoint, params=None):
    headers = {
        "Authorization": f"Token token={os.getenv('PAGERDUTY_API_KEY')}",
        "Accept": "application/vnd.pagerduty+json;version=2",
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{PAGERDUTY_BASE_URL}/{endpoint}", headers=headers, params=params) as response:
            if response.status != 200:
                raise Exception(f"PagerDuty API error: {response.status} - {await response.text()}")
            return await response.json()
