from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from apikey import api_data

app = Flask(__name__)

genai.configure(api_key=api_data)
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    query = data.get("query", "")
    response = model.generate_content(query)
    return jsonify({"answer": response.text})

@app.route("/flashcards", methods=["POST"])
def flashcards():
    data = request.get_json()
    topic = data.get("topic", "")
    prompt = f"Generate 5 flashcards for '{topic}' in this format:\nQuestion: ...\nAnswer: ..."

    response = model.generate_content(prompt)
    lines = response.text.split("\n")
    flashcards = []
    q, a = "", ""

    for line in lines:
        if line.lower().startswith("question:"):
            q = line.split(":", 1)[1].strip()
        elif line.lower().startswith("answer:"):
            a = line.split(":", 1)[1].strip()
            flashcards.append({"question": q, "answer": a})

    return jsonify(flashcards)

if __name__ == "__main__":
    app.run(debug=True)
