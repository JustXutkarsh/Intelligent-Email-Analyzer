from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
import json

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI(title="Intelligent Email Analyzer API")

# Allow Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Schema
class EmailRequest(BaseModel):
    id: str
    text: str


# ---------- Helper Functions ----------

def ask_openai(prompt, temperature=0.2):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    return response.choices[0].message.content.strip()


# ---------- Endpoints ----------

@app.get("/")
def home():
    return {"message": "Welcome to Intelligent Email Analyzer API"}


@app.post("/summarize")
def summarize_email(data: EmailRequest):
    prompt = f"""
    Summarize the following email in 2–3 crisp lines:

    EMAIL:
    {data.text}
    """
    result = ask_openai(prompt)
    return {"summary": result}


@app.post("/bias")
def detect_bias(data: EmailRequest):
    prompt = f"""
    Analyze for bias in the following email. 
    Return only a short explanation.

    EMAIL:
    {data.text}
    """
    result = ask_openai(prompt)
    return {"bias_analysis": result}


@app.post("/sentiment")
def sentiment(data: EmailRequest):
    prompt = f"""
    Give a sentiment score between -1 and +1 for the following email,
    and explain briefly.

    EMAIL:
    {data.text}
    """
    result = ask_openai(prompt)
    return {"sentiment": result}


@app.post("/classify")
def classify(data: EmailRequest):
    prompt = f"""
    Classify this email as one of: Work, Personal, Spam, Urgent, Support.

    EMAIL:
    {data.text}
    """
    result = ask_openai(prompt)
    return {"classification": result}


@app.post("/spam-detection")
def spam_detector(data: EmailRequest):
    prompt = f"""
    Determine if the following email is spam. Return "Spam" or "Not Spam".

    EMAIL:
    {data.text}
    """
    result = ask_openai(prompt)
    return {"spam_result": result}


@app.post("/assistant/followup")
def follow_up(data: EmailRequest):
    prompt = f"""
    Analyze whether this email requires a follow-up. 
    Return ONLY valid JSON in this exact structure:

    {{
        "needs_followup": true/false,
        "followup_reason": "",
        "suggested_timeframe": "",
        "action_items": []
    }}

    EMAIL:
    {data.text}

    Make sure the JSON is valid. Do NOT add explanations.
    """
    result = ask_openai(prompt, temperature=0.3)

    # Send raw output so Streamlit can parse it
    return {"analysis": result}
