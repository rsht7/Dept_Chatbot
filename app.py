from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import get_answer  # Import from chatbot.py

app = Flask(__name__)
CORS(app)  # Allows requests from frontend (Next.js)

max_inp_words = 50 
# POST endpoint for the chatbot
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "Query is missing"}), 400
    
    if len(query.strip().split()) > max_inp_words:
        return jsonify({"error": f"Query exceeds {max_inp_words} words limit"}), 400

    try:
        response = get_answer(query)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
