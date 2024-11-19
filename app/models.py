# models.py
from flask_sqlalchemy import SQLAlchemy
from .extensions import db

# Association table for services and teams
service_team = db.Table(
    'service_team',
    db.Column('service_id', db.String(64), db.ForeignKey('service.id'), primary_key=True),
    db.Column('team_id', db.String(64), db.ForeignKey('team.id'), primary_key=True)
)

class Service(db.Model):
    """Represents an entity that is monitored, such as a web service."""
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)

    # Relationships
    escalation_policy_id = db.Column(db.String(64), db.ForeignKey('escalation_policy.id'))
    escalation_policy = db.relationship('EscalationPolicy', back_populates='services')
    incidents = db.relationship('Incident', backref='service', lazy=True)
    teams = db.relationship('Team', secondary=service_team, back_populates='services')


class Team(db.Model):
    """Represents a group of users within the organization."""
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    # Relationships
    services = db.relationship('Service', secondary=service_team, back_populates='teams')


class Incident(db.Model):
    """Represents a problem or issue within a service."""
    id = db.Column(db.String(64), primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    status = db.Column(db.String(128), nullable=False)

    # Relationships
    service_id = db.Column(db.String(64), db.ForeignKey('service.id'), nullable=False)


class EscalationPolicy(db.Model):
    """Defines the notification sequence for incidents."""
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    # Relationships
    services = db.relationship('Service', back_populates='escalation_policy')
