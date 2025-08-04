FROM python:3.11-slim

WORKDIR /app

COPY update/update_client.py .
COPY shared ./shared

RUN pip install flask psycopg2-binary flask_cors



CMD ["python", "update_client.py"]

