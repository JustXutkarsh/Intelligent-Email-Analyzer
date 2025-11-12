.

🧠 Intelligent Email Analyzer
AI-powered email summarization, sentiment analysis, bias detection, classification, spam detection & follow-up suggestion assistant.

This project combines:

FastAPI backend (deployed on Render)

Streamlit frontend (deployed on Streamlit Cloud)

OpenAI GPT-based models

A clean modular architecture

Multiple ML/NLP features

It provides a complete intelligent email analysis tool for productivity, support teams, and automated email triage.

🚀 Live Demo (Frontend)

👉 Streamlit App: Add your Streamlit URL here
https://intelligent-email-analyzer-14.streamlit.app

🖥️ API (Backend)

👉 Backend API URL:
https://intelligent-email-analyzer.onrender.com

✨ Features
📝 Email Summarization

Generates clear, compact summaries of long or complex emails.

⚖️ Bias Detection

Identifies emotional or political bias in text.

Useful for corporate communication and sensitive responses.

❤️ Sentiment Analysis

Returns a sentiment score from -1 (negative) to +1 (positive).

Includes a short explanation.

🏷 Email Classification

Categorizes the email into:

Work

Personal

Urgent

Support

Spam

🚫 Spam Detection

Determines whether the email is spam or legitimate

🌐 Fully Deployed

Backend on Render

Frontend on Streamlit Cloud

Both connected via public API URL

📁 Project Structure
intelligent-email-analyzer/
│
├── main.py                # FastAPI backend
├── app.py                 # Streamlit frontend (optional in same repo)
├── requirements.txt       # Dependencies
│
├── utils/                 # Helper modules
│   ├── summarization.py
│   ├── preprocess.py
│   ├── bias_detection.py
│
├── data/
│   └── emails.csv         # Sample data (optional)
│
└── README.md

⚙️ Backend Setup (FastAPI)
1️⃣ Install dependencies
pip install -r requirements.txt
2️⃣ Add your OpenAI API key

Create .env:
OPENAI_API_KEY=your_key_here
3️⃣ Run the FastAPI server
uvicorn main:app --reload
4️⃣ Test API
Open in browser:
http://127.0.0.1:8000
⚙️ Frontend Setup (Streamlit)
1️⃣ Run Streamlit app
streamlit run app.py
2️⃣ Make sure FASTAPI_URL in app.py is correct:
FASTAPI_URL = "https://intelligent-email-analyzer.onrender.com"
☁️ Deployment Guide
🔵 Deploy Backend (Render)

Push project to GitHub

Go to https://render.com

Create New → Web Service

Connect GitHub repo

Set:

Start Command:

uvicorn main:app --host 0.0.0.0 --port 10000


Build Command:

pip install -r requirements.txt


Add environment variable:

OPENAI_API_KEY=your-key


Deploy

Copy backend URL (e.g., https://intelligent-email-analyzer.onrender.com)

🟣 Deploy Frontend (Streamlit Cloud)

Go to https://share.streamlit.io

Deploy GitHub repo

In app.py, set:

FASTAPI_URL = "https://intelligent-email-analyzer.onrender.com"


Deploy

🧪 Test Example Email
Hi Riya,

Please share the updated quotation for the 50 transformer units we discussed 
last week. Also confirm whether the delivery can still be completed before 
the 28th, as our client timeline is very strict.

Thanks,
Utkarsh


Expected output:

Summary ✔

Bias: Neutral ✔

Sentiment: Slightly positive ✔

Classification: Work ✔

Spam: Not Spam ✔

Follow-up JSON ✔

📌 Notes

Uses OpenAI GPT-4o-mini for fast, cheap inference.

Render free tier sleeps after 15 minutes — first request may take a few seconds.

Can easily expand with:
Email priority scoring
Auto-reply draft generation
PDF email export
Multi-language support

live link- https://intelligent-email-analyzer-14.streamlit.app/

💡 Author

Utkarsh Pandey
AI Engineer | Data Science Learner | Innovator
📍 Pune, India
💼 GitHub: https://github.com/JustXutkarsh

✉️ Email: utkarshp034@gmail.com
