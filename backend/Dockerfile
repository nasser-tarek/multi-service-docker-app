FROM python:3.10-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y gcc libpq-dev
RUN pip install --prefix=/install -r requirements.txt
FROM python:3.10-slim as runtime
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .
CMD ["python", "app.py"]
