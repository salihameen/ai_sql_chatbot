import streamlit as st
import requests

st.set_page_config(page_title="AI → SQL Chatbot", layout="centered")
st.title("AI → SQL Chatbot (Demo)")

text = st.text_area("Ask a question about the database", height=150)

if st.button("Run"):
    if not text.strip():
        st.warning("Enter a question.")
    else:
        try:
            resp = requests.post("http://localhost:5000/query", json={"text": text}, timeout=10)
            if resp.ok:
                data = resp.json()
                st.subheader("Generated SQL")
                st.code(data.get("sql", ""))
                st.subheader("Results")
                st.write(data.get("results", []))
            else:
                st.error(resp.text)
        except Exception as e:
            st.error(str(e))
