import logging
import json
import requests

from app.telegram.api_methods import (
    prepare_url,
    select_send_method,
)
from app.telegram.payload_router import select_payload_method

logger = logging.getLogger(__name__)


def handle_forwarded(post, BOT_TOKEN):
    post_type = "forwarded"
    send_method = select_send_method(post_type)
    url = prepare_url(send_method, BOT_TOKEN)
    process_payload_method = select_payload_method(post_type)
    payload = process_payload_method(post)
    response = requests.post(url, json=payload or {})
    logger.warning("Response: %s", response.text)
    return {"statusCode": 200, "body": json.dumps({"message": "OK"})}
