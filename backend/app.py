from flask import Flask, jsonify, request, render_template
from pathlib import Path
import os

from services.password_analyzer import analyze_password
from services.password_generator import generate_password
from services.analytics import AnalyticsStore
from services.policy_checker import check_policy

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "analytics.db"

app = Flask(__name__, template_folder="../frontend", static_folder="../frontend/static")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

analytics = AnalyticsStore(DB_PATH)

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/api/analyze")
def api_analyze():
    data = request.get_json(silent=True) or {}
    password = data.get("password")

    if not isinstance(password, str):
        return jsonify({"error": "Password must be supplied as a string."}), 400
    if len(password) > 128:
        return jsonify({"error": "Password exceeds the supported 128-character limit."}), 400

    # The password is intentionally never logged, persisted, or returned.
    context = data.get("context") or {}
    result = analyze_password(password, context)

    # Store only safe aggregate metadata.
    analytics.record_analysis(result)
    return jsonify(result)

@app.get("/api/dashboard/stats")
def dashboard_stats():
    return jsonify(analytics.stats())

@app.get("/api/analytics/weaknesses")
def analytics_weaknesses():
    return jsonify(analytics.weaknesses())

@app.post("/api/generate-password")
def api_generate_password():
    data = request.get_json(silent=True) or {}
    try:
        length = int(data.get("length", 20))
    except (TypeError, ValueError):
        return jsonify({"error": "Length must be an integer."}), 400

    if length < 16 or length > 128:
        return jsonify({"error": "Generator length must be between 16 and 128."}), 400

    options = {
        "uppercase": bool(data.get("uppercase", True)),
        "lowercase": bool(data.get("lowercase", True)),
        "digits": bool(data.get("digits", True)),
        "symbols": bool(data.get("symbols", True)),
    }
    if not any(options.values()):
        return jsonify({"error": "Select at least one character type."}), 400

    generated = generate_password(length=length, **options)
    return jsonify({"password": generated})

@app.post("/api/policy/check")
def api_policy():
    data = request.get_json(silent=True) or {}
    password = data.get("password")
    if not isinstance(password, str):
        return jsonify({"error": "Password must be supplied as a string."}), 400

    policy = data.get("policy") or {}
    result = check_policy(password, policy)
    return jsonify(result)

@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "password-strength-analyzer"})

if __name__ == "__main__":
    app.run(debug=True)
