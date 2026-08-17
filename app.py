from flask import Flask, jsonify, render_template_string
import time
import os

app = Flask(__name__)
START_TIME = time.time()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MK Cloud Production Service</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: #1e293b; padding: 2rem; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); width: 420px; border: 1px solid #334155; }
        h1 { font-size: 1.4rem; color: #38bdf8; margin-bottom: 0.5rem; }
        .badge { display: inline-block; padding: 0.25rem 0.6rem; border-radius: 9999px; font-size: 0.8rem; font-weight: 600; background: #059669; color: #ecfdf5; margin-bottom: 1rem; }
        .metric { display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #334155; font-size: 0.9rem; }
        .metric:last-child { border-bottom: none; }
        .label { color: #94a3b8; }
        .val { font-weight: 500; color: #e2e8f0; }
    </style>
</head>
<body>
    <div class="card">
        <h1>MK Cloud Service By Momin Khisal</h1>
        <div class="badge">● SYSTEM ACTIVE</div>
        <div class="metric"><span class="label">Environment:</span><span class="val">{{ env }}</span></div>
        <div class="metric"><span class="label">Uptime:</span><span class="val">{{ uptime }}s</span></div>
        <div class="metric"><span class="label">Status:</span><span class="val">200 OK</span></div>
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    uptime = int(time.time() - START_TIME)
    env = os.getenv("APP_ENV", "production")
    return render_template_string(HTML_TEMPLATE, uptime=uptime, env=env)

@app.route("/api/status")
def status():
    return jsonify({
        "status": "healthy",
        "service": "MK-cloud-app",
        "uptime_seconds": int(time.time() - START_TIME),
        "version": os.getenv("APP_VERSION", "1.0.0")
    }), 200

@app.route("/api/metrics")
def metrics():
    return jsonify({
        "status_code": 200,
        "active_threads": 1,
        "memory_state": "normal"
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
