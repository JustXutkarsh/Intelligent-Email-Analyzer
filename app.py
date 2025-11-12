# --- Path Fix: ensures we can import from project root ---
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Standard Imports ---
import streamlit as st
import requests
import json
import re
from utils.google_calendar import (
    do_local_oauth,
    load_credentials,
    create_event,
    parse_timeframe_to_datetime,
)

FASTAPI_URL = "http://127.0.0.1:8000"

# --- Streamlit Page Config ---
st.set_page_config(
    page_title="Intelligent Email Analyzer",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- Header ---
st.title("🧠 Intelligent Email Analyzer")
st.markdown(
    """
    Analyze your emails for **summary**, **bias**, **sentiment**, **classification**, **spam**,  
    and get **Follow-Up Suggestions** with direct **Google Calendar integration**. 📅
    """
)

# --- Input Area ---
email_text = st.text_area(
    "✉️ Paste your email below:",
    height=220,
    placeholder="e.g., Hi Riya, please share the final invoice and confirm delivery by Friday...",
)

# --- Buttons ---
col1, col2, col3 = st.columns(3)
analyze = col1.button("🔍 Analyze Email")
clear = col2.button("🧹 Clear All")
connect_google = col3.button("🔗 Connect Google Calendar")

# --- Handle Google Calendar Connection ---
if connect_google:
    with st.spinner("Opening Google OAuth flow..."):
        try:
            creds = do_local_oauth()
            st.success("✅ Google Calendar connected successfully.")
        except Exception as e:
            st.error(f"Google OAuth failed: {e}")

if clear:
    st.experimental_rerun()

# --- Check Google Auth Status ---
creds = load_credentials()
if creds:
    st.sidebar.success("✅ Google Calendar Connected")
else:
    st.sidebar.warning("⚠️ Google Calendar not connected")

# --- Main Analysis Logic ---
if analyze and email_text.strip():
    with st.spinner("Analyzing email with AI..."):
        try:
            summarize = requests.post(f"{FASTAPI_URL}/summarize", json={"id": "1", "text": email_text})
            bias = requests.post(f"{FASTAPI_URL}/bias", json={"id": "1", "text": email_text})
            sentiment = requests.post(f"{FASTAPI_URL}/sentiment", json={"id": "1", "text": email_text})
            classify = requests.post(f"{FASTAPI_URL}/classify", json={"id": "1", "text": email_text})
            spam = requests.post(f"{FASTAPI_URL}/spam-detection", json={"id": "1", "text": email_text})
            followup = requests.post(f"{FASTAPI_URL}/assistant/followup", json={"id": "1", "text": email_text})

            if all(res.status_code == 200 for res in [summarize, bias, sentiment, classify, spam, followup]):
                st.success("✅ Analysis Complete")

                # --- Summary ---
                st.subheader("📄 Summary")
                st.write(summarize.json()["summary"])

                # --- Bias Analysis ---
                st.subheader("⚖️ Bias Analysis")
                st.info(bias.json()["bias_analysis"])

                # --- Sentiment ---
                st.subheader("❤️ Sentiment")
                st.write(sentiment.json()["sentiment"])

                # --- Classification ---
                st.subheader("🏷️ Classification")
                st.write(classify.json()["classification"])

                # --- Spam Detection ---
                st.subheader("🚫 Spam Detection")
                st.write(spam.json()["spam_result"])

                # --- Follow-Up & To-Do Suggestions ---
                st.subheader("📆 Follow-Up & To-Do Suggestions")
                follow_data = followup.json()
                analysis = follow_data.get("analysis", "")

                try:
                    # Remove Markdown formatting before parsing
                    clean_json = re.sub(r"```(json)?", "", analysis).strip()
                    parsed = json.loads(clean_json)

                    if parsed.get("needs_followup"):
                        st.success("✅ This email likely needs a follow-up.")
                        if "followup_reason" in parsed:
                            st.write(f"**Reason:** {parsed['followup_reason']}")
                        if "suggested_timeframe" in parsed:
                            st.write(f"**Suggested timeframe:** {parsed['suggested_timeframe']}")
                        if "action_items" in parsed and parsed["action_items"]:
                            st.markdown("**Action Items:**")
                            for item in parsed["action_items"]:
                                st.write(f"- {item}")

                        # --- Download .ics Reminder ---
                        if follow_data.get("calendar_file") and os.path.exists(follow_data["calendar_file"]):
                            with open(follow_data["calendar_file"], "rb") as f:
                                st.download_button(
                                    label="⬇️ Download Follow-Up Reminder (.ics)",
                                    data=f,
                                    file_name=follow_data["calendar_file"],
                                    mime="text/calendar",
                                )

                        # --- Sync to Google Calendar ---
                        if creds:
                            if st.button("📥 Sync Follow-Up to Google Calendar"):
                                try:
                                    timeframe = parsed.get("suggested_timeframe", "")
                                    start_dt = parse_timeframe_to_datetime(timeframe)
                                    summary = parsed.get("followup_reason", "Email Follow-Up")
                                    description = "Action items:\n" + "\n".join(parsed.get("action_items", []))
                                    created = create_event(
                                        summary=summary,
                                        description=description,
                                        start_dt=start_dt,
                                        duration_minutes=30,
                                    )
                                    st.success("✅ Event created successfully on Google Calendar.")
                                    st.markdown(f"[Open in Calendar]({created.get('htmlLink')})")
                                except Exception as e:
                                    st.error(f"Failed to create event: {e}")
                        else:
                            st.info("🔗 Connect Google Calendar to sync this follow-up automatically.")
                    else:
                        st.info("No follow-up required for this email.")
                except Exception:
                    st.warning("⚠️ Could not parse structured JSON. Showing raw output:")
                    st.code(analysis)
            else:
                st.error("❌ One or more endpoints failed. Check backend logs.")
        except requests.exceptions.ConnectionError:
            st.error("🚫 Could not connect to FastAPI. Is it running on port 8000?")

elif analyze and not email_text.strip():
    st.warning("⚠️ Please enter text before analyzing.")


