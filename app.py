from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/authorize", methods=["POST"])
def authorize():
    data = request.get_json(silent=True)

    print("\n==============================")
    print("Time:", datetime.now().isoformat())
    print("Data received by backend:")
    print(data)

    if not data:
        return jsonify({
            "success": False,
            "message": "No data received"
        }), 400

    # Display-only mode (no blockchain action)
    return jsonify({
        "success": True,
        "message": "Backend received successfully (display only, no blockchain action)"
    })

if __name__ == "__main__":
    print("🚀 Local frontend-backend service started")
    print("Visit: http://localhost:8080")
    app.run(host="0.0.0.0", port=8080, debug=True)
