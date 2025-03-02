FROM python:3.11-slim-buster

WORKDIR /flask-crypto-app

# Copy requirements first to take advantage of Docker caching
COPY requirements.txt .

# Upgrade pip with --break-system-packages to prevent permission issues
RUN python -m pip install --upgrade --no-cache-dir pip --break-system-packages

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Set environment variables
ENV FLASK_APP=app
ENV FLASK_ENV=development

# Expose the Flask port
EXPOSE 5000

# Ensure entrypoint script is executable
RUN chmod +x ./entrypoint.sh

# Use sh as the entrypoint
ENTRYPOINT [ "sh", "./entrypoint.sh" ]

# Default command to run the Flask app
CMD ["python3", "run.py"]
