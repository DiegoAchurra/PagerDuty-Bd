FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Environment variables for Flask
ENV FLASK_APP=app
ENV FLASK_ENV=production

# Start the app
CMD flask run --host=0.0.0.0 --port=5000
