import time
import random
import os
from flask import Flask, jsonify, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

APP_ENV = os.getenv("APP_ENV", "local")

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["endpoint"]
)

ERROR_COUNT = Counter(
    "http_errors_total",
    "Total HTTP errors",
    ["endpoint"]
)


@app.route("/")
def index():
    REQUEST_COUNT.labels(method="GET", endpoint="/", status="200").inc()
    return jsonify({"status": "ok", "env": APP_ENV})


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/ready")
def ready():
    return jsonify({"status": "ready"}), 200


@app.route("/slow")
def slow():
    delay = random.uniform(0.1, 2.5)
    time.sleep(delay)

    if random.random() < 0.15:
        ERROR_COUNT.labels(endpoint="/slow").inc()
        REQUEST_COUNT.labels(method="GET", endpoint="/slow", status="500").inc()
        REQUEST_LATENCY.labels(endpoint="/slow").observe(delay)
        return jsonify({"error": "simulated failure"}), 500

    REQUEST_COUNT.labels(method="GET", endpoint="/slow", status="200").inc()
    REQUEST_LATENCY.labels(endpoint="/slow").observe(delay)
    return jsonify({"latency_s": round(delay, 3)}), 200


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
