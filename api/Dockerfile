FROM python:3.11-slim
LABEL authors="pazimor"

WORKDIR /app
ENV PYTHONPATH=/app

COPY api.py .
COPY sql/ ./sql

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 4201

CMD ["python", "api.py"]