from flask import Flask, request, jsonify, render_template
from datetime import datetime
import json

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

    # Save to local file
    try:
        with open("received_data.txt", "a", encoding="utf-8") as f:
            f.write(f"Time: {datetime.now().isoformat()}\n")
            # Use single line JSON for easier parsing
            f.write(f"Data: {json.dumps(data, ensure_ascii=False)}\n")
            f.write("==============================\n")
    except Exception as e:
        print(f"Error saving to file: {e}")

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

@app.route("/admin/data")
def view_data():
    records = []
    try:
        with open("received_data.txt", "r", encoding="utf-8") as f:
            # Parse the custom text format into a list of dicts
            current_record = {}
            for line in f:
                line = line.strip()
                if line.startswith("Time:"):
                    if current_record:
                        records.append(current_record)
                    current_record = {"time": line.replace("Time:", "").strip()}
                elif line.startswith("Data:"):
                    try:
                        data_json = line.replace("Data:", "").strip()
                        current_record["data"] = json.loads(data_json)
                    except:
                        current_record["data"] = {"error": "Invalid JSON"}
            if current_record:
                records.append(current_record)
    except FileNotFoundError:
        pass
    
    # Reverse to show newest first
    records.reverse()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Data View</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: #f0f2f5; padding: 20px; }
            h1 { color: #1a1a1a; }
            .card { background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; overflow: hidden; }
            .card-header { background: #f8f9fa; padding: 12px 20px; border-bottom: 1px solid #e9ecef; color: #666; font-size: 0.9em; font-weight: 600; display: flex; justify-content: space-between; }
            .card-body { padding: 20px; }
            .data-row { display: flex; margin-bottom: 10px; border-bottom: 1px solid #eee; padding-bottom: 10px; }
            .data-row:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
            .label { width: 150px; font-weight: 600; color: #444; flex-shrink: 0; }
            .value { color: #1a1a1a; word-break: break-all; font-family: monospace; font-size: 1.1em; }
            .empty { color: #888; font-style: italic; }
            .refresh-btn { position: fixed; bottom: 20px; right: 20px; background: #007bff; color: white; padding: 12px 24px; border-radius: 30px; text-decoration: none; box-shadow: 0 4px 12px rgba(0,123,255,0.3); font-weight: bold; transition: transform 0.2s; }
            .refresh-btn:hover { transform: translateY(-2px); }
        </style>
    </head>
    <body>
        <h1>Received Data Log</h1>
        <div id="container">
    """
    
    if not records:
        html += '<p class="empty">No data received yet.</p>'
    
    for rec in records:
        html += f"""
        <div class="card">
            <div class="card-header">
                <span>Received Time</span>
                <span>{rec.get('time', 'Unknown')}</span>
            </div>
            <div class="card-body">
        """
        data = rec.get("data", {})
        if isinstance(data, dict):
            for k, v in data.items():
                html += f"""
                <div class="data-row">
                    <span class="label">{k}</span>
                    <span class="value">{v}</span>
                </div>
                """
        else:
             html += f"<pre>{data}</pre>"
        
        html += """
            </div>
        </div>
        """

    html += """
        </div>
        <a href="/admin/data" class="refresh-btn">🔄 Refresh Data</a>
    </body>
    </html>
    """
    
    return html

if __name__ == "__main__":
    print("🚀 Local frontend-backend service started")
    print("Visit: http://localhost:8083")
    app.run(host="0.0.0.0", port=8083, debug=True)
