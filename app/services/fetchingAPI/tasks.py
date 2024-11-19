import os
import json
import asyncio
from .utils import fetch_pagerduty_data
from app.models import Team, Service, Incident, EscalationPolicy, db

async def fetch_and_save_teams():
    """Fetch teams from PagerDuty API and save them into the database."""
    try:
        data = await fetch_pagerduty_data("teams")
        teams = data.get("teams", [])
    except Exception as e:
        print(f"Error fetching teams from API: {e}")
        incidents = []

    for team_data in teams:
        team = Team.query.get(team_data["id"])
        if not team:
            team = Team(id=team_data["id"], name=team_data["name"])
            db.session.add(team)
        else:
            if team.name != team_data["name"]:
                team.name = team_data["name"]

        db.session.commit()


async def fetch_and_save_services():
    """Fetch services from PagerDuty API and save them into the database."""
    try:
        data = await fetch_pagerduty_data("services")
        services = data.get("services", [])
    except Exception as e:
        print(f"Error fetching services from API: {e}")
        incidents = []

    for service_data in services:
        # Handle escalation policy
        escalation_policy = None
        escalation_policy_data = service_data.get("escalation_policy")
        if escalation_policy_data:
            escalation_policy = EscalationPolicy.query.get(escalation_policy_data["id"])
            if not escalation_policy:
                escalation_policy = EscalationPolicy(
                    id=escalation_policy_data["id"],
                    name=escalation_policy_data["summary"],
                )
                db.session.add(escalation_policy)
            else:
                if escalation_policy.name != escalation_policy_data["summary"]:
                    escalation_policy.name = escalation_policy_data["summary"]

        # Handle service
        service = Service.query.get(service_data["id"])
        if not service:
            service = Service(
                id=service_data["id"],
                name=service_data["name"],
                description=service_data.get("description"),
                escalation_policy=escalation_policy,
            )
            db.session.add(service)
        else:
            if (service.name != service_data["name"] or
                service.description != service_data.get("description") or
                service.escalation_policy != escalation_policy):
                service.name = service_data["name"]
                service.description = service_data.get("description")
                service.escalation_policy = escalation_policy

        # Associate teams with the service
        for team_data in service_data.get("teams", []):
            team = Team.query.get(team_data["id"])
            if not team:
                team = Team(id=team_data["id"], name=team_data["summary"])
                db.session.add(team)
            if team not in service.teams:
                service.teams.append(team)

        db.session.commit()


async def fetch_and_save_incidents():
    """Fetch incidents from PagerDuty API and save them into the database."""
    try:
        data = await fetch_pagerduty_data("incidents")
        incidents = data.get("incidents", [])
    except Exception as e:
        print(f"Error fetching incidents from API: {e}")
        incidents = []

    # Use mock data if no incidents are fetched
    if not incidents:
        print("No incidents fetched from API. Loading mock data...")
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Absolute path of the current file
        mock_file_path = os.path.join(base_dir, '..', '..', 'static', 'json', 'mock_incidents.json')
        try:
            with open(mock_file_path, 'r') as mock_file:
                mock_data = json.load(mock_file)
                incidents = mock_data.get("incidents", [])
        except FileNotFoundError:
            print(f"Mock data file not found at {mock_file_path}.")
            return
        except json.JSONDecodeError as e:
            print(f"Error parsing mock data: {e}")
            return

    # Save or update incidents
    for incident_data in incidents:
        incident = Incident.query.get(incident_data["id"])
        if not incident:
            incident = Incident(
                id=incident_data["id"],
                title=incident_data["title"],
                status=incident_data["status"],
                service_id=incident_data["service"]["id"],
            )
            db.session.add(incident)
        else:
            if (incident.title != incident_data["title"] or
                incident.status != incident_data["status"] or
                incident.service_id != incident_data["service"]["id"]):
                incident.title = incident_data["title"]
                incident.status = incident_data["status"]
                incident.service_id = incident_data["service"]["id"]

    db.session.commit()
    print(f"Fetched or loaded {len(incidents)} incidents.")


async def fetch_and_save_escalation_policies():
    """Fetch escalation policies from PagerDuty API and save them into the database."""
    try:
        data = await fetch_pagerduty_data("escalation_policies")
        escalation_policies = data.get("escalation_policies", [])
    except Exception as e:
        print(f"Error fetching escalation policies from API: {e}")
        incidents = []

    for policy_data in escalation_policies:
        policy = EscalationPolicy.query.get(policy_data["id"])
        if not policy:
            policy = EscalationPolicy(
                id=policy_data["id"],
                name=policy_data["summary"]
            )
            db.session.add(policy)
        else:
            if policy.name != policy_data["summary"]:
                policy.name = policy_data["summary"]

        db.session.commit()
