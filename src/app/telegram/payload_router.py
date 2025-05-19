from app.telegram.payloads.single import (
    process_text_payload,
    process_photo_payload,
    process_video_payload,
)


def select_payload_method(post_type):
    payload_method_config = {
        "text": process_text_payload,
        "photo": process_photo_payload,
        "video": process_video_payload,
    }
    return payload_method_config.get(post_type)
