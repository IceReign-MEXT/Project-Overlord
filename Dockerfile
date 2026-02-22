# Dockerfile for Project Juggernaut
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY . .
# The command to start the Juggernaut Engine
CMD ["python", "juggernaut_engine.py"]
