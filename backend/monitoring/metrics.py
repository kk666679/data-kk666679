from prometheus_client import Counter, Histogram, generate_latest
import time

# Metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')

def track_metrics(method: str, endpoint: str):
    REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()

def get_metrics():
    return generate_latest()