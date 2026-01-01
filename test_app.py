from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/')
def root():
    return "ok"

@app.route('/api/submit', methods=['POST'])
def submit():
    data = request.get_json(silent=True)
    print("received:", data)
    return jsonify({"ok": True, "received": data})
