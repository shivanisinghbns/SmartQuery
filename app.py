from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from services.ollama_mongo_generator import get_collections_from_prompt
from services.mongo_query import fetch_data_from_mongo

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")  # Assumes templates/index.html exists

@app.route("/query", methods=["POST"])
def query():
    try:
        question = request.json.get("question", "")

        # Step 1: Ask model to extract collection(s) + filter
        collections, filter_dict = get_collections_from_prompt(question)

        # Step 2: Run MongoDB query
        results = fetch_data_from_mongo(collections, filter_dict)

        return jsonify({
            "collections": collections,
            "filter": filter_dict,
            "results": results
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=8000, debug=True)
