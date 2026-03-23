import streamlit as st
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

st.title("🧠 AI Medical MCQ Generator")

topic = st.text_input("Enter topic (e.g. Myocardial Infarction)")

if st.button("Generate 15 MCQs"):
    if topic:
        with st.spinner("Generating questions..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": f"Generate 15 NEET PG level MCQs on {topic} with 4 options and correct answer."}
                ]
            )

            st.write(response.choices[0].message.content)
    else:
        st.warning("Please enter a topic")
