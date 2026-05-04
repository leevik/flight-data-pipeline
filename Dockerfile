FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY src ./src

# Without apache airflow start with this script
# CMD ["python", "-m", "src.extract.fetch_flights"]