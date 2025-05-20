from app.config.constants import TARGET_CHAT_ID


def process_photo_payload(post):
    photo = max(post.get("photo", []), key=lambda p: p["file_size"])
    return {
        "chat_id": TARGET_CHAT_ID,
        "photo": photo["file_id"],
        "caption": post.get("caption", ""),
        "caption_entities": post.get("caption_entities", []),
        "disable_web_page_preview": True,
    }


def process_video_payload(post):
    video = post.get("video", {})
    return {
        "chat_id": TARGET_CHAT_ID,
        "video": video.get("file_id", ""),
        "caption": post.get("caption", ""),
        "caption_entities": post.get("caption_entities", []),
        "disable_web_page_preview": True,
    }


def process_text_payload(post):
    return {
        "chat_id": TARGET_CHAT_ID,
        "text": post.get("text", ""),
        "entities": post.get("entities", []),
        "disable_web_page_preview": True,
    }


def process_forwarded_payload(post):
    original_channel = post["chat"].get("title", "Quelle")
    text = post.get("text", "")
    final_text = f"🔁 Weitergeleitet von {original_channel}:\n\n{text}"
    return {
        "chat_id": TARGET_CHAT_ID,
        "from_chat_id": post["chat"]["id"],
        "text": final_text,
        "disable_web_page_preview": True,
    }
