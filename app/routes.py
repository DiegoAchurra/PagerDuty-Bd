# routes.py
import pandas as pd
from datetime import datetime
from flask import Blueprint, jsonify, render_template, make_response
from app.services.dashboard.tasks import get_total_services, get_incidents_per_service, get_incidents_by_service_status, get_team_service_counts, get_escalation_policy_counts, get_most_incidents_data

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """
    Render the dashboard index page with all data.
    """
    try:
        # Fetch all required data
        total_services = get_total_services()
        incidents_per_service_list = get_incidents_per_service()
        incidents_by_service_status_list = get_incidents_by_service_status()
        team_service_package = get_team_service_counts()
        escalation_policy_counts = get_escalation_policy_counts()
        most_incidents_data, graph_data = get_most_incidents_data()

        # Build data package
        data = {
            "package1_total_services": total_services,
            "package2_incidents_per_service": incidents_per_service_list,
            "package3_incidents_by_service_status": incidents_by_service_status_list,
            "package4_team_service_counts": team_service_package,
            "package5_escalation_policy_counts": escalation_policy_counts,
            "package6_csv_report_data": {
                "package1_total_services": total_services,
                "package2_incidents_per_service": incidents_per_service_list,
                "package3_incidents_by_service_status": incidents_by_service_status_list,
                "package4_team_service_counts": team_service_package,
                "package5_escalation_policy_counts": escalation_policy_counts,
            },
            "package7_most_incidents_data": most_incidents_data,
            "package8_graph_data": graph_data
        }

        return render_template('base.html', data=data, year=datetime.now().year)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/download/csv')
def download_csv():
    try:
        data = {
            "Total Services": [get_total_services()],
            "Incidents Per Service": [get_incidents_per_service()],
            "Incidents by Service and Status": [get_incidents_by_service_status()],
            "Teams and Related Services": [get_team_service_counts()],
            "Escalation Policies": [get_escalation_policy_counts()],
        }

        dfs = {key: pd.DataFrame(value) for key, value in data.items()}
        result = pd.concat(dfs.values(), keys=dfs.keys(), axis=1)

        response = make_response(result.to_csv(index=False))
        response.headers["Content-Disposition"] = "attachment; filename=dashboard_data.csv"
        response.headers["Content-Type"] = "text/csv"
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500