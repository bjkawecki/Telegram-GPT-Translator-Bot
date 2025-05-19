from src.config.constants import TARGET_CHAT_ID


def process_photo_payload(post):
    photo = max(post.get("photo", []), key=lambda p: p["file_size"])
    return {
        "chat_id": TARGET_CHAT_ID,
        "photo": photo["file_id"],
        "caption": post.get("caption", ""),
        "caption_entities": post.get("caption_entities", []),
    }


def process_video_payload(post):
    video = post.get("video", {})
    return {
        "chat_id": TARGET_CHAT_ID,
        "video": video.get("file_id", ""),
        "caption": post.get("caption", ""),
        "caption_entities": post.get("caption_entities", []),
    }


def process_text_payload(post):
    return {
        "chat_id": TARGET_CHAT_ID,
        "text": post.get("text", ""),
        "entities": post.get("entities", []),
    }
