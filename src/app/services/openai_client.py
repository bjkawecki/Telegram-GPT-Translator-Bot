import logging

from openai import OpenAI

from app.config.aws_resources import openai_api_key
from app.config.constants import SYSTEM_PROMPT

client = OpenAI(api_key=openai_api_key)
logger = logging.getLogger()


def translate_text(text: str, target_lang: str = "Deutsch") -> str:
    logger.warning("Zu übersetzen: %s", text)
    prompt = f"Übersetze den folgenden Text nach {target_lang}:\n\n{text}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )
    logger.warning("OpenAI Antwort: %s", response)
    return response.choices[0].message.content
