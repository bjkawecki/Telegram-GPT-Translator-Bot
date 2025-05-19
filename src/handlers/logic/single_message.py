import json

import requests

from src.telegram.api_methods import prepare_url, select_send_method
from src.telegram.message_classifier import find_post_type
from src.telegram.payload_router import select_payload_method


def handle_single_post(post):
    post_type = find_post_type(post)
    send_method = select_send_method(post_type)
    url = prepare_url(send_method)
    process_payload_method = select_payload_method(post_type)
    payload = process_payload_method(post)
    response = requests.post(url, json=payload or {})
    print(f"Sent single post ({post_type}):", response.status_code)
    return {"statusCode": 200, "body": json.dumps({"message": "OK"})}
