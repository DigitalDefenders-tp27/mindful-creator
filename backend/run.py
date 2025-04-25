import os
import sys
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

# ─── Load environment variables from backend/.env ───────────────────────────
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# ─── Bring in your nlp‑model code ───────────────────────────────────────────
nlp_src = os.path.abspath(os.path.join(basedir, '../nlp-model/src'))
if nlp_src not in sys.path:
    sys.path.insert(0, nlp_src)

# ─── Import your inference + LLM handlers ────────────────────────────────────
from inference import predict_text
from llm_handlers import generate_positive_response, generate_toxicity_responses
from common.constants import TOXICITY_THRESHOLD

# ─── Configure OpenAI key ───────────────────────────────────────────────────
openai.api_key = os.getenv('OPENAI_API_KEY')

# ─── Create Flask app and enable CORS for your frontend ─────────────────────
app = Flask(__name__)
frontend_origin = os.getenv('CORS_ORIGIN', '*')  # should match your .env CORS_ORIGIN
CORS(app, resources={r"/api/*": {"origins": frontend_origin}})

# ─── /api/chatbot: your existing LLM endpoint ───────────────────────────────
@app.route("/api/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json(force=True) or {}
    user_input = data.get("message", "")
    prompt = (
        "You are a kind assistant for digital wellbeing and comment response tips.\n"
        f"User: {user_input}\nAssistant:"
    )
    try:
        resp = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        reply = resp.choices[0].text.strip()
    except Exception as e:
        app.logger.error(f"OpenAI error: {e}")
        reply = "Sorry, I couldn't respond right now."
    return jsonify({"reply": reply})

# ─── /api/analyze_comment: sentiment + toxicity + strategy ────────────────
@app.route("/api/analyze_comment", methods=["POST"])
def analyze_comment():
    data = request.get_json(force=True) or {}
    text = data.get("text") or data.get("comment")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    # 1) run your in‑house model
    analysis = predict_text(text)

    # 2) pick highest‐prob toxicity label
    tox = analysis.get("toxicity_details", {})
    highest_label, info = max(tox.items(), key=lambda x: float(x[1]["probability"]))
    prob = float(info["probability"])

    # 3) call LLM handler
    if prob > TOXICITY_THRESHOLD:
        strategy = generate_toxicity_responses(text, highest_label, prob)
    else:
        strategy = generate_positive_response(text)

    return jsonify({
        "analysis": analysis,
        "strategy": strategy
    })

# ─── Launch ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.getenv("BACKEND_PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
