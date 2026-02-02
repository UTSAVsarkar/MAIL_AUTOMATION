from bs4 import BeautifulSoup
import re

def clean_email_text(html_text, max_chars=1200):
    """
    Converts HTML email to clean, readable plain text
    and truncates safely for LLM input.
    """

    # Parse HTML
    soup = BeautifulSoup(html_text, "html.parser")

    # Remove scripts, styles, images
    for tag in soup(["script", "style", "img", "a"]):
        tag.decompose()

    # Get text
    text = soup.get_text(separator=" ")

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Hard truncate (VERY IMPORTANT)
    return text[:max_chars]