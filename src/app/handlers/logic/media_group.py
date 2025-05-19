import json

import requests

from app.telegram.groups.storage import (
    store_media_group_item,
    get_media_group,
    delete_media_group,
)
from app.telegram.groups.payload_builder import process_media_group_payload
from app.telegram.api_methods import prepare_url


def handle_media_group(post, media_group_id, BOT_TOKEN):
    message_id = post["message_id"]
    store_media_group_item(media_group_id, message_id, post)

    items = get_media_group(media_group_id)
    if len(items) < 2:
        print(f"Media group {media_group_id} waiting for more items...")
        return {"statusCode": 200, "body": json.dumps({"message": "Waiting"})}

    posts = [item["post"] for item in items]
    payload = process_media_group_payload(posts)
    url = prepare_url("sendMediaGroup", BOT_TOKEN)
    response = requests.post(url, json=payload)
    print("Sent media group:", response.status_code)
    delete_media_group(media_group_id)
    return {"statusCode": 200, "body": json.dumps({"message": "Media group sent"})}
