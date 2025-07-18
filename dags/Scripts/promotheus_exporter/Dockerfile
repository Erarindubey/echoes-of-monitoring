FROM python:3.10-slim

WORKDIR /exporter

COPY metrics.py .

RUN apt-get update && apt-get install -y procps curl

RUN pip install prometheus_client flask

EXPOSE 9100
EXPOSE 9200

CMD ["python", "metrics.py"]