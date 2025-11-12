from fastapi import FastAPI
from pydantic import BaseModel
import openai, os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from utils.summarization import summarize_email
from utils.bias_detection import detect_bias
from utils.calendar_event import create_ics_event

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI(title="Intelligent Email Analyzer")

# --- Allow Streamlit to connect locally ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Request schema ---
class EmailRequest(BaseModel):
    id: str
    text: str


@app.get("/")
def home():
    return {"message": "Welcome to Intelligent Email Analyzer API"}


# 🧠 Summarization
@app.post("/summarize")
async def summarize(data: EmailRequest):
    return {"id": data.id, "summary": summarize_email(data.text)}


# ⚖️ Bias Detection
@app.post("/bias")
async def bias(data: EmailRequest):
    return {"id": data.id, "bias_analysis": detect_bias(data.text)}


# ❤️ Sentiment Analysis
@app.post("/sentiment")
async def sentiment(data: EmailRequest):
    prompt = f"""
    Analyze the emotional sentiment of the following email.
    Give a sentiment score between -1 (negative) and +1 (positive),
    and a short reasoning.
    Email: {data.text}
    """
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return {"id": data.id, "sentiment": response.choices[0].message.content.strip()}


# 🏷️ Email Classification
@app.post("/classify")
async def classify(data: EmailRequest):
    prompt = f"""
    Classify this email as one of [Work, Personal, Spam, Support, Urgent].
    Provide a one-line justification.
    Email: {data.text}
    """
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return {"id": data.id, "classification": response.choices[0].message.content.strip()}


# 🚫 Spam Detection
@app.post("/spam-detection")
async def spam_detection(data: EmailRequest):
    prompt = f"""
    Determine if the following email is spam or legitimate.
    Return either 'Spam' or 'Not Spam' with a brief reason.
    Email: {data.text}
    """
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return {"id": data.id, "spam_result": response.choices[0].message.content.strip()}


# 📆 Follow-Up Assistant
@app.post("/assistant/followup")
async def followup(data: EmailRequest):
    """
    Determines if the email requires follow-up, extracts tasks,
    and suggests an ideal follow-up time window.
    """
    prompt = f"""
    Analyze the following email and return a JSON object with:
    1. "needs_followup": true/false
    2. "followup_reason": short text
    3. "suggested_timeframe": e.g. "2 days", "next week"
    4. "action_items": list of to-dos (if any)
    Email:
    {data.text}
    Return valid JSON only.
    """

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    analysis = response.choices[0].message.content.strip()

    # Create a default .ics event if follow-up is needed
    if '"needs_followup": true' in analysis.lower():
        filename = create_ics_event("Email Follow-Up", days_from_now=2)
        return {
            "id": data.id,
            "analysis": analysis,
            "calendar_file": filename,
        }
    else:
        return {"id": data.id, "analysis": analysis, "calendar_file": None}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
