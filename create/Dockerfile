FROM python:3.11-slim

WORKDIR /app

COPY create/create_client.py .
COPY shared ./shared

RUN pip install flask psycopg2-binary flask_cors



CMD ["python", "create_client.py"]
