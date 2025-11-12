import streamlit as st
import requests
import json
import re

FASTAPI_URL = "http://127.0.0.1:8000"
  # update if deployed

st.set_page_config(
    page_title="Intelligent Email Analyzer",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Intelligent Email Analyzer")
st.markdown("""
Analyze your emails for **summary**, **bias**, **sentiment**,  
**classification**, **spam detection**, and **follow-up suggestions**.
""")

email_text = st.text_area(
    "✉️ Paste your email:",
    height=200,
    placeholder="Write or paste an email here..."
)

col1, col2 = st.columns(2)
analyze = col1.button("🔍 Analyze Email")
clear = col2.button("🧹 Clear")

if clear:
    st.experimental_rerun()

if analyze and not email_text.strip():
    st.warning("⚠️ Please enter text before analyzing.")
elif analyze:
    with st.spinner("Analyzing email..."):
        try:
            summary = requests.post(f"{FASTAPI_URL}/summarize", json={"id":"1","text":email_text})
            bias = requests.post(f"{FASTAPI_URL}/bias", json={"id":"1","text":email_text})
            sentiment = requests.post(f"{FASTAPI_URL}/sentiment", json={"id":"1","text":email_text})
            classify = requests.post(f"{FASTAPI_URL}/classify", json={"id":"1","text":email_text})
            spam = requests.post(f"{FASTAPI_URL}/spam-detection", json={"id":"1","text":email_text})
            follow = requests.post(f"{FASTAPI_URL}/assistant/followup", json={"id":"1","text":email_text})

            if any(r.status_code != 200 for r in [summary, bias, sentiment, classify, spam, follow]):
                st.error("❌ Some endpoints failed. Check your FastAPI server.")
            else:
                st.success("✔ Analysis complete!")

                st.subheader("📄 Summary")
                st.write(summary.json()["summary"])

                st.subheader("⚖ Bias Analysis")
                st.write(bias.json()["bias_analysis"])

                st.subheader("❤️ Sentiment")
                st.write(sentiment.json()["sentiment"])

                st.subheader("🏷 Classification")
                st.write(classify.json()["classification"])

                st.subheader("🚫 Spam Detection")
                st.write(spam.json()["spam_result"])

                st.subheader("📆 Follow-Up Suggestions")

                raw = follow.json().get("analysis", "")

                # clean markdown fences
                cleaned = re.sub(r"```json|```", "", raw).strip()

                try:
                    parsed = json.loads(cleaned)

                    if parsed.get("needs_followup"):
                        st.success("✔ This email requires follow-up.")
                        st.write(f"**Reason:** {parsed.get('followup_reason','')}")
                        st.write(f"**Suggested timeframe:** {parsed.get('suggested_timeframe','')}")

                        actions = parsed.get("action_items", [])
                        if actions:
                            st.markdown("**Action Items:**")
                            for a in actions:
                                st.write("- " + a)
                    else:
                        st.info("No follow-up needed.")

                except Exception:
                    st.warning("⚠ Could not parse follow-up JSON. Showing raw output:")
                    st.code(raw)

        except requests.exceptions.ConnectionError:
            st.error("🚫 Could not connect to FastAPI. Is it running?")





