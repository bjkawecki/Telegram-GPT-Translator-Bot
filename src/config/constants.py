import os

SSM_PARAM_BOT_TOKEN = "/mirrowchan_bot/bot_token"
SSM_PARAM_WEBHOOK_URL = "/mirrowchan_bot/api_gateway_url"
TARGET_CHAT_ID = "@test_kanal_output"

ENV = os.environ.get("APP_ENV", "dev")  # Fallback zu 'dev', wenn nicht gesetzt

IS_PROD = ENV == "prod"
IS_DEV = ENV == "dev"
