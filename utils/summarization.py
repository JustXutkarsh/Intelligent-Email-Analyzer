import openai
from utils.preprocess import clean_email

def summarize_email(text: str) -> str:
    clean_text = clean_email(text)
    prompt = f"Summarize the following email in 2-3 short, factual sentences:\n\n{clean_text}"
    
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    return response.choices[0].message.content.strip()
