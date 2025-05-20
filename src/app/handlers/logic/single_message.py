import json
import logging

import requests

from app.telegram.api_methods import prepare_url, select_send_method
from app.telegram.message_classifier import find_post_type
from app.telegram.payload_router import select_payload_method

logger = logging.getLogger(__name__)


def handle_single_post(post, BOT_TOKEN, forwarded=False):
    post_type = find_post_type(post)
    logger.warning("post_type: %s", post_type)
    send_method = select_send_method(post_type)
    url = prepare_url(send_method, BOT_TOKEN)
    process_payload_method = select_payload_method(post_type)
    logger.warning("process_payload_method: %s", process_payload_method)
    payload = process_payload_method(post, forwarded)
    response = requests.post(url, json=payload or {})
    print(f"Sent single post ({post_type}):", response.status_code)
    return {"statusCode": 200, "body": json.dumps({"message": "OK"})}
