from app.config.constants import TARGET_CHAT_ID

import re


def escape_markdown(text: str) -> str:
    escape_chars = r"_*\[\]()~`>#+-=|{}.!"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)


def make_clickable_forwarded_text(original_channel: str, text: str) -> str:
    escaped_text = escape_markdown(text)
    escaped_channel = escape_markdown(original_channel)
    return f"*[🔁 Weitergeleitet aus {escaped_channel}](https://t.me/{original_channel})*\n\n{escaped_text}"


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
    original_channel = post.get("forward_origin", {}).get("chat", {}).get("title")
    text = post.get("text", "")
    return {
        "chat_id": TARGET_CHAT_ID,
        "from_chat_id": post["chat"]["id"],
        "text": make_clickable_forwarded_text(original_channel, text),
        "entities": post.get("entities", []),
        "parse_mode": "MarkdownV2",
        "disable_web_page_preview": True,
    }
