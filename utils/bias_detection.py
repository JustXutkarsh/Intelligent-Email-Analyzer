import openai
from utils.preprocess import clean_email

def detect_bias(text: str) -> str:
    clean_text = clean_email(text)
    prompt = f"""
    Detect any emotional or political bias in this text. 
    Give a bias score between 0 (neutral) and 1 (highly biased) 
    and explain the reasoning briefly.
    
    Text:
    {clean_text}
    """

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()
