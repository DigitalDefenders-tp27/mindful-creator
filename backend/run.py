from app import create_app
from flask import request, jsonify
from flask_cors import CORS
import openai

openai.api_key = "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"

@app.route("/api/chatbot", methods=["POST"])
def chatbot():
    data = request.json
    user_input = data.get("message", "")

    prompt = f"You are a kind assistant for digital wellbeing and comment response tips.\nUser: {user_input}\nAssistant:"

    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        return jsonify({"reply": response.choices[0].text.strip()})
    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "Sorry, I couldn't respond right now."}), 500

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000) 