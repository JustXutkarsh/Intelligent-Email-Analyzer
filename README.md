🧠 Intelligent Email Analyzer

AI-powered Email Summarizer, Classifier & Follow-Up Assistant with Google Calendar Integration

📌 Overview

Intelligent Email Analyzer is an advanced NLP-powered tool that helps users manage their inbox efficiently.
It automatically:

Summarizes emails

Detects bias, tone, and sentiment

Classifies the type (Work / Personal / Spam / Support)

Extracts action items

Suggests if follow-up is needed

Generates .ics calendar reminders or syncs directly to Google Calendar

Built using:

⚡ FastAPI for the backend

💻 Streamlit for the interactive frontend

🧠 OpenAI GPT-4o-mini for natural language analysis

🗓️ Google Calendar API for scheduling automation

🚀 Features
Category	Features
🧠 Intelligence	Email summarization, sentiment & bias detection, tone classification
⚙️ Automation	Follow-up detection, task extraction, event scheduling
📆 Integration	Google Calendar OAuth + event creation
📨 Spam Filtering	Classify emails as Spam / Legitimate
🧾 Output Options	Downloadable .ics reminders, live calendar sync
💬 Future Add-ons	Auto-reply generator, task sync (Notion/Todoist), analytics dashboard


🏗️ Project Structure
intelligent_email_analyzer/
├── main.py                        # FastAPI backend
├── .env                           # API keys and environment variables
├── client_secrets.json             # Google OAuth credentials
├── utils/
│   ├── summarization.py            # Email summarization logic
│   ├── bias_detection.py           # Bias analysis logic
│   ├── calendar_event.py           # Local .ics calendar generation
│   └── google_calendar.py          # Google Calendar integration
└── streamlit_app/
    └── app.py                      # Streamlit frontend UI


⚙️ Installation & Setup
1️⃣ Clone Repository
git clone https://github.com/yourusername/intelligent-email-analyzer.git
cd intelligent-email-analyzer

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # (Mac/Linux)
venv\Scripts\activate      # (Windows)

3️⃣ Install Dependencies
pip install -r requirements.txt

🔑 Environment Variables
Create a .env file in the project root:
OPENAI_API_KEY=your_openai_key_here

🗓️ Google Calendar Setup

Go to Google Cloud Console

Create a project → Enable Google Calendar API

Create OAuth Client ID (type: Desktop App)

Download JSON → rename to client_secrets.json → place in project root

First time you click “Connect Google Calendar”, a browser OAuth flow opens.
→ A token.json file will be saved for reuse.

🖥️ Running the App
1️⃣ Start Backend 
uvicorn main:app --reload
Open http://127.0.0.1:8000/docs
 to verify FastAPI is running.


2️⃣ Start Frontend
streamlit run streamlit_app/app.py
Then visit http://localhost:8501
 to use the UI.

 🧠 Usage Flow

Paste an email into the Streamlit textbox
Click 🔍 Analyze Email
View:

Summary

Bias & Sentiment

Classification

Spam Detection

Follow-Up Suggestions

Download .ics reminder or

Sync directly to Google Calendar via OAuth

🧪 Example Input
Hi Riya,
Could you please send the final project report and confirm delivery by Friday?
Thanks,
Utkarsh

Expected Output

Summary: Request for project report & confirmation
Sentiment: +0.4 (Polite)
Classification: Work
Follow-Up: true
Action Items:
Send report
Confirm delivery

Google Calendar event auto-created for Friday

🧭 Credits

OpenAI GPT Models

FastAPI

Streamlit

Google Calendar API

💡 Author

Utkarsh Pandey
AI Engineer | Data Science Learner | Innovator
📍 Pune, India
💼 GitHub: https://github.com/JustXutkarsh
✉️ Email: utkarshp034@gmail.com