FROM python:3.11-slim

WORKDIR /app

COPY read/read_clients.py .
COPY shared ./shared

RUN pip install flask psycopg2-binary flask_cors



CMD ["python", "read_clients.py"]
