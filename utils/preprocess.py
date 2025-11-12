import re

def clean_email(text: str) -> str:
    """
    Removes signatures, multiple line breaks, and URLs from emails.
    """
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[-_]{2,}.*", "", text)
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()
