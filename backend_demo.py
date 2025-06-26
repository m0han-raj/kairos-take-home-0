from flask import Flask, request, jsonify
from flask_cors import CORS
from agent_host.agent import run_agent
import logging

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
CORS(app, resources={r"/search": {"origins": "*"}})

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Invalid request. 'query' is required."}), 400

    query = data['query'].strip()
    if not query:
        return jsonify({"papers": []})

    try:
        final_output = None
        for output in run_agent(query):
            if "tool_output" in output:
                final_output = output["tool_output"]
        
        if final_output is not None:
            return jsonify({"papers": final_output})
        else:
            logging.warning("Agent did not produce a final output for query: %s", query)
            return jsonify({"papers": [], "error": "Agent did not produce a final output."})

    except Exception as e:
        logging.exception("An error occurred during search for query: %s", query)
        return jsonify({"error": f"An internal error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True, threaded=True)