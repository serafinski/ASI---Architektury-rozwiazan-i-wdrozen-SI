FROM apache/airflow:2.10.2-python3.11

# Install system dependencies
USER root
RUN apt-get update && \
    apt-get install -y \
    unzip \
    libgomp1 \
    docker.io && \
    rm -rf /var/lib/apt/lists/*

# Add airflow user to docker group
RUN groupadd -f docker && \
    usermod -aG docker airflow

# Copy requirements.txt
COPY requirements.txt /requirements.txt

# Switch to airflow user and install packages
USER ${AIRFLOW_UID:-50000}
RUN pip install -r /requirements.txt

# Return to airflow user
USER ${AIRFLOW_UID:-50000}:0

# Set proper permissions for Docker socket
RUN chmod 666 /var/run/docker.sock || true