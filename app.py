from flask import Flask, jsonify
import json
from pathlib import Path

app = Flask(__name__)

OUTPUT_DIR = Path(__file__).parent.resolve() / "output"

def load_contests(platform):
    try:
        with open(OUTPUT_DIR / f"{platform}_contests.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"error": "File not found"}

@app.route('/contests/<platform>', methods=['GET'])
def get_contests(platform):
    contests = load_contests(platform)
    return jsonify(contests)

