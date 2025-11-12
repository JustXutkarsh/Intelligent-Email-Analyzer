from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# OpenAI client (new SDK)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

def ask_openai(prompt: str, temperature: float = 0.2):
    """
    Safely call the OpenAI API using the new official client.
    Fully compatible with Render & latest SDK.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        # print error to logs
        print("OPENAI ERROR:", str(e))
        return f"ERROR: Failed to call OpenAI: {str(e)}"


# ---------- Endpoints ----------

@app.get("/")
def home():
    return {"message": "Welcome to Intelligent Email Analyzer API"}


@app.post("/summarize")
def summarize_email(data: EmailRequest):
    prompt = f"""
    Summarize this email in 2–3 crisp lines:

    EMAIL:
    {data.text}
    """
    result = ask_openai(prompt)
    return {"summary": result}


@app.post("/bias")
def detect_bias(data: EmailRequest):
    prompt = f"""
    Analyze for bias in the following email.

    EMAIL:
    {data.text}
    """
    result = ask_openai(prompt)
    return {"bias_analysis": result}


@app.post("/sentiment")
def check_sentiment(data: EmailRequest):
    prompt = f"""
    Give a sentiment analysis score between -1 and +1.
    Also provide 1–2 lines of reasoning.

    EMAIL:
    {data.text}
    """
    result = ask_openai(prompt)
    return {"sentiment": result}


@app.post("/classify")
def classify_email(data: EmailRequest):
    prompt = f"""
    Classify this email as one of:
    Work, Personal, Spam, Urgent, Support.

    EMAIL:
    {data.text}
    """
    result = ask_openai(prompt)
    return {"classification": result}


@app.post("/spam-detection")
def spam_detector(data: EmailRequest):
    prompt = f"""
    Determine whether the email is spam.
    Return ONLY "Spam" or "Not Spam".

    EMAIL:
    {data.text}
    """
    result = ask_openai(prompt)
    return {"spam_result": result}


@app.post("/assistant/followup")
def follow_up(data: EmailRequest):
    prompt = f"""
    Examine the email and decide if it requires follow-up.

    Respond ONLY with valid JSON:
    {{
        "needs_followup": true/false,
        "followup_reason": "",
        "suggested_timeframe": "",
        "action_items": []
    }}

    EMAIL:
    {data.text}
    """

    result = ask_openai(prompt, temperature=0.3)
    return {"analysis": result}

