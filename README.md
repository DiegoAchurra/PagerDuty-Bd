
# PagerDuty Dashboard Backend

This repository contains the backend implementation for a PagerDuty dashboard that aggregates and analyzes PagerDuty data, storing it in a MySQL database. It supports fetching data from the PagerDuty API, storing it in the database, and generating reports for analysis.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies](#technologies)
- [Setup](#setup)
- [Project Structure](#project-structure)
- [Endpoints](#endpoints)
- [Issues](#issues)
- [Running Tests](#running-tests)

## Overview

The backend application processes and stores data from PagerDuty API endpoints to allow detailed analysis of:

- Services and incidents
- Team associations
- Escalation policies
- Incident statistics

The application also generates CSV reports and visualizations to aid in data interpretation.

## Features

- **Data Aggregation**: Fetches and processes data from PagerDuty API.
- **Database Modeling**: Uses SQLAlchemy to model Services, Incidents, Teams, and Escalation Policies.
- **CSV Export**: Provides downloadable reports summarizing data.
- **Visualization**: Generates graphs to illustrate incident statistics.
- **Unit and Integration Testing**: Thorough test coverage using `pytest`.

## Technologies

- **Backend Framework**: Flask
- **Frontend Technologies**: HTML, CSS, and JavaScript
- **Database**: MySQL with SQLAlchemy ORM
- **API**: Asynchronous calls using `aiohttp`
- **Testing**: `pytest` and `pytest-asyncio`
- **Containerization**: Docker and Docker Compose
- **Data Processing**: Pandas

## Setup

### Prerequisites

- Docker and Docker Compose
- Python 3.10 or above
- MySQL database

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/DiegoAchurra/PagerDuty-Bd.git
   cd PagerDuty-Bd
   ```

2. **Set Up Environment Variables**:
   Create a `.env` file in the root directory with the following content:
   ```env
   MYSQL_USER=root
   MYSQL_PASSWORD=rootpassword
   MYSQL_DB=pagerduty_db
   MYSQL_HOST=db
   PAGERDUTY_API_KEY=your_api_key
   PAGERDUTY_BASE_URL=instance_or_default_url
   ```

3. **Build and Run Docker Containers**:
   ```bash
   docker-compose up --build
   ```

4. **Access the Application**:
   The app will be available at `http://localhost:5000`.

## Project Structure

```
.
├── app/
│   ├── extensions.py          # Initializes extensions (e.g., SQLAlchemy)
│   ├── models.py              # Database models
│   ├── routes.py              # Application routes to services
│   ├── services/              # Business logic and data-fetching scripts
│   │   ├── dashboard/ 	       # Logic for aggregating dashboard data
│   │   └── fetchingAPI/       # Utilities for fetching data from PagerDuty API
│   ├── static/                # Static assets like CSS and mock JSON
│   └── templates/             # HTML templates for rendering
├── config.py                  # Configuration file
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker setup for the application
├── docker-compose.yml         # Docker Compose setup for multi-container setup
├── tests/                     # Test files using pytest
└── README.md                  # Documentation
```

## Endpoints

- **GET `/`**: Main dashboard with all aggregated data.
- **GET `/download/csv`**: Download a CSV report summarizing the dashboard data.

## Issues

- While working on the project, we realize that the API normally does not provide incidents data, which is crucial for this exercise. To address this, we implemented a fallback mechanism in the incident-fetching service. If the API response comes empty, the service is programmed to use mock data.

## Running Tests

The project includes unit and integration tests for models, routes, and services.

1. **Run All Tests**:
   ```bash
   pytest -v
   ```
