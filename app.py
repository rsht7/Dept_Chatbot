from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import get_answer  # Import from chatbot.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_limiter.errors import RateLimitExceeded
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
CORS(app)  # Allows requests from frontend (Next.js)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day"]
)

# ✅ Limit this endpoint: 10 requests per 8 hours per IP

max_inp_words = 50 

# ✅ Handle rate-limit error globally
@app.errorhandler(RateLimitExceeded)
def handle_rate_limit(e):
    return jsonify({"error": "You’ve reached your daily usage limit 🔒 Please try again later."}), 429


# POST endpoint for the chatbot
@app.route("/chat", methods=["POST"])
@limiter.limit("5 per 8 hours")
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
