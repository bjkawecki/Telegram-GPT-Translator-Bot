from openai import OpenAI
import logging
from app.config.aws_resources import openai_api_key

client = OpenAI(api_key=openai_api_key)
logger = logging.getLogger()


def translate_text(text: str, target_lang: str = "Deutsch") -> str:
    logger.warning("Zu übersetzen: %s", text)
    prompt = f"Übersetze den folgenden Text nach {target_lang}:\n\n{text}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Du bist ein professioneller Übersetzer."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content
