import os

class Config:
    # Database settings
    MYSQL_HOST = os.getenv('MYSQL_HOST', '127.0.0.1')  # Default to localhost
    if os.getenv('RUNNING_IN_DOCKER'):
        MYSQL_HOST = os.getenv('MYSQL_HOST', 'db')  # Use 'db' when running in Docker

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@"
        f"{MYSQL_HOST}/{os.getenv('MYSQL_DB', 'test_db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # API settings
    PAGERDUTY_BASE_URL = os.getenv('PAGERDUTY_BASE_URL')
    PAGERDUTY_API_KEY = os.getenv('PAGERDUTY_API_KEY')
