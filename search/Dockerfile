FROM python:3.11-slim

WORKDIR /app

COPY search/search_by_id.py .
COPY shared ./shared

RUN pip install flask psycopg2-binary flask_cors



CMD ["python", "search_by_id.py"]
