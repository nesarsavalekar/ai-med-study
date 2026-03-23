from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

# ✅ Secure API key from Render environment
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# ✅ Temporary study text (no PDF needed for now)
def extract_text():
    return """
Acute myocardial infarction results from coronary artery occlusion.
The wavefront of necrosis progresses from subendocardium to subepicardium.
Reactive oxygen species and inflammatory mediators contribute to myocardial injury.
Plaque rupture and thrombosis are key initiating events.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    difficulty = request.json.get("difficulty", "normal")

    text = extract_text()

    if difficulty == "hardcore":
        prompt = f"""
Generate 10 VERY DIFFICULT NEET PG level MCQs.

Rules:
- Clinical case-based
- Integrated concepts
- Very tricky options
- Include explanation

Text:
{text}
"""
    else:
        prompt = f"""
Generate 15 NEET PG level MCQs.

Rules:
- Concept-based
- Clear options
- Include explanation

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
