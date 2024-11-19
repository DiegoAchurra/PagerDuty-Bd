from app.models import Service, Incident, Team, EscalationPolicy, service_team
from app import db

def get_total_services():
    """Fetch the total number of services."""
    return Service.query.count()


def get_incidents_per_service():
    """Fetch the number of incidents per service."""
    incidents = (
        db.session.query(Service.id, Service.name, db.func.coalesce(db.func.count(Incident.id), 0))
        .outerjoin(Incident, Incident.service_id == Service.id)
        .group_by(Service.id, Service.name)
        .all()
    )
    return [{"id": service_id, "name": service_name, "count": count} for service_id, service_name, count in incidents]


def get_incidents_by_service_status():
    """Fetch the number of incidents by service and status."""
    statuses = ["triggered", "acknowledged", "resolved"]
    service_status_template = {status: 0 for status in statuses}

    results = []
    for service in Service.query.all():
        status_counts = service_status_template.copy()
        incidents_by_service = (
            db.session.query(Incident.status, db.func.count(Incident.id))
            .filter(Incident.service_id == service.id)
            .group_by(Incident.status)
            .all()
        )
        for status, count in incidents_by_service:
            status_counts[status] = count
        results.append({
            "id": service.id,
            "name": service.name,
            "status_counts": status_counts
        })
    return results


def get_team_service_counts():
    """Fetch the count of teams and their related services."""
    teams_query = Team.query.all()
    team_service_counts = [
        {
            "id": team.id,
            "name": team.name,
            "services": [{"id": service.id, "name": service.name} for service in team.services]
        }
        for team in teams_query
    ]
    return {"teams_count": len(team_service_counts), "teams": team_service_counts}


def get_escalation_policy_counts():
    """Fetch escalation policies with related teams and services."""
    escalation_policies_query = (
        db.session.query(
            EscalationPolicy.id,
            EscalationPolicy.name,
            Team.id.label("team_id"),
            Team.name.label("team_name"),
            Service.id.label("service_id"),
            Service.name.label("service_name")
        )
        .outerjoin(Service, EscalationPolicy.id == Service.escalation_policy_id)
        .outerjoin(service_team, service_team.c.service_id == Service.id)
        .outerjoin(Team, Team.id == service_team.c.team_id)
        .all()
    )

    escalation_policies = {}
    for ep_id, ep_name, team_id, team_name, service_id, service_name in escalation_policies_query:
        if ep_id not in escalation_policies:
            escalation_policies[ep_id] = {
                "id": ep_id,
                "name": ep_name,
                "teams": [],
                "services": []
            }
        if team_id and {"id": team_id, "name": team_name} not in escalation_policies[ep_id]["teams"]:
            escalation_policies[ep_id]["teams"].append({"id": team_id, "name": team_name})
        if service_id and {"id": service_id, "name": service_name} not in escalation_policies[ep_id]["services"]:
            escalation_policies[ep_id]["services"].append({"id": service_id, "name": service_name})

    return {
        "count": len(escalation_policies),
        "details": list(escalation_policies.values())
    }


def get_most_incidents_data():
    """Fetch the service with the most incidents and details by status."""
    statuses = ["triggered", "acknowledged", "resolved"]

    most_incidents_service = (
        db.session.query(Service.name, Service.id, db.func.count(Incident.id))
        .outerjoin(Incident, Incident.service_id == Service.id)
        .group_by(Service.name, Service.id)
        .order_by(db.func.count(Incident.id).desc())
        .first()
    )

    if most_incidents_service:
        most_service_name, most_service_id, most_service_count = most_incidents_service
        incidents_by_status = {
            status: [
                {"id": incident.id, "title": incident.title}
                for incident in Incident.query.filter_by(service_id=most_service_id, status=status).all()
            ]
            for status in statuses
        }
    else:
        most_service_name, most_service_count, incidents_by_status = None, 0, {}

    graph_data = {
        "title": f"Incident Distribution for {most_service_name}" if most_service_name else "No Data",
        "data": [
            {"status": status, "count": len(incidents_by_status.get(status, []))}
            for status in statuses
        ]
    }

    most_incidents_data = {
        "service_name": most_service_name,
        "incident_count": most_service_count,
        "incidents_by_status": incidents_by_status
    }

    return most_incidents_data, graph_data