import google.generativeai as genai
import streamlit as st

# 1. Connect to Gemini using your verified key and latest model
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-flash-latest")

# 2. Page Setup
st.set_page_config(page_title="Mentor Sentence Machine", page_icon="📝")
st.title("Mentor Sentence Machine 📝")
st.write(
    "Write an original sentence that mimics the exact grammar, rhythm, and clause structure of the model."
)

# 3. Default Cisneros sentence
default_benchmark = (
    "When the light in her aunt’s room goes out, Marin lights a cigarette, "
    "and it doesn’t matter if it’s cold out or if the radio doesn’t work or "
    "if we’ve got nothing to say to each other."
)

# 4. Text input boxes
model_sentence = st.text_area(
    "Model Sentence (Benchmark):", value=default_benchmark, height=100
)
student_sentence = st.text_area(
    "Your Imitation Sentence:",
    placeholder="Type your imitation sentence here...",
    height=100,
)

# 5. Grading Button
if st.button("Evaluate Structure"):
    if not student_sentence.strip():
        st.warning("Please type a sentence first!")
    else:
        with st.spinner("Analyzing syntactic architecture..."):
            prompt = f"""
            You are an encouraging high school English teacher evaluating sentence imitation.
            
            MODEL SENTENCE:
            "{model_sentence}"
            
            STUDENT SENTENCE:
            "{student_sentence}"
            
            Evaluate how closely the student matches the syntactic structure of the model sentence.
            Do NOT grade based on vocabulary, tone, or story topic. Grade exclusively on:
            1. Clause types (time clauses, main clauses, conditional clauses, etc.).
            2. Clause order and pacing.
            3. Parallel structure and conjunction repetition (e.g., repeating 'if', 'or').
            4. Punctuation patterns.
            
            Format your response strictly using these Markdown headings:
            ### Match Score: [Give an integer percentage from 0 to 100]%
            
            **What You Matched Well:**
            [1-2 sentences highlighting what they matched well structurally]
            
            **Revision Tip:**
            [1-2 sentences showing what structural element was missing or out of order, and how to adjust it]
            """

            try:
                response = model.generate_content(prompt)
                st.write("---")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Something went wrong: {e}")