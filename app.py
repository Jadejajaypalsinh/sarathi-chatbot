from flask import Flask, request, jsonify, render_template
from groq import Groq

app = Flask(__name__)

# 🔑 YOUR GROQ API KEY
import os
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)
# Load knowledge
try:
    with open("knowledge.txt", "r", encoding="utf-8") as file:
        knowledge = file.read()
except:
    knowledge = "No knowledge available."


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": f"""
You are SARATHI - Offline Data Synchronization Assistant.

Rules:
- Answer ONLY from provided knowledge
- Keep answers simple and clear
- Use bullet points where possible
- If answer not found, say: "I don't have that information in my knowledge base."

Knowledge:
{knowledge}
"""
                },
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})


if __name__ == "__main__":
    app.run(debug=True)