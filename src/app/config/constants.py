import os

SSM_PARAM_BOT_TOKEN = "/mirrowchan_bot/bot_token"
SSM_PARAM_WEBHOOK_URL = "/mirrowchan_bot/api_gateway_url"
TARGET_CHAT_ID = "@test_kanal_output"
SOURCE_CHAT_ID = "@test_kanal_input"

ENV = os.environ.get("APP_ENV", "dev")  # Fallback zu 'dev', wenn nicht gesetzt

IS_PROD = ENV == "prod"
IS_DEV = ENV == "dev"

ALLOWED_CHANNEL_ID = -1002611172833

SSM_OPENAI_KEY_PARAM = "/mirrowchan_bot/openai_api_key"

DYNAMODB_TABLE_NAME = "MediaGroupBuffer"


SYSTEM_PROMPT = "Du bist ein professioneller, neutraler Übersetzer.\
    Übersetze den eingegebenen Text exakt und vollständig in die gewünschte Zielsprache.\
    Gib ausschließlich die Übersetzung zurück – ohne Anmerkungen, Korrekturen, Erklärungen oder Kommentare.\
    Wenn die Übersetzung eindeutig nicht möglich ist, gib nur das Wort 'Übersetzungsfehler' zurück."
