from flask import Flask, render_template, request, jsonify
import fitz  # PyMuPDF
import os
from openai import OpenAI

app = Flask(__name__)

# ✅ SECURE API KEY (from Render env variable)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

PDF_PATH = "robbins.pdf"

def extract_text():
    doc = fitz.open(PDF_PATH)
    text = ""
    for page in doc:
        text += page.get_text()
    return text[:4000]  # limit for API

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    difficulty = request.json.get("difficulty", "normal")

    text = extract_text()

    if difficulty == "hardcore":
        prompt = f"""
Generate 10 VERY DIFFICULT NEET PG level MCQs from this text.

- Concept integration
- Clinical scenarios
- Twisted options
- High difficulty

Text:
{text}
"""
    else:
        prompt = f"""
Generate 15 NEET PG level MCQs from this text.

Text:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return jsonify({"mcqs": response.choices[0].message.content})

if __name__ == "__main__":
    app.run(debug=True)