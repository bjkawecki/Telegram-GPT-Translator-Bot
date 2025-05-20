from app.config.constants import TARGET_CHAT_ID
from app.telegram.formatting import make_clickable_forwarded_text
from app.services.openai_client import translate_text


def process_photo_payload(post, forwarded=False):
    photo = max(post.get("photo", []), key=lambda p: p["file_size"])
    payload = {
        "chat_id": TARGET_CHAT_ID,
        "photo": photo["file_id"],
        "caption": post.get("caption", ""),
        "caption_entities": post.get("caption_entities", []),
        "disable_web_page_preview": True,
    }
    if not forwarded:
        return payload
    original_channel = post.get("forward_origin", {}).get("chat", {}).get("title")
    caption = post.get("caption", "")
    payload["parse_mode"] = "MarkdownV2"
    payload["caption"] = make_clickable_forwarded_text(original_channel, caption)
    return payload


def process_video_payload(post, forwarded=False):
    video = post.get("video", {})
    payload = {
        "chat_id": TARGET_CHAT_ID,
        "video": video.get("file_id", ""),
        "caption": post.get("caption", ""),
        "caption_entities": post.get("caption_entities", []),
        "disable_web_page_preview": True,
    }
    if not forwarded:
        return payload
    original_channel = post.get("forward_origin", {}).get("chat", {}).get("title")
    caption = post.get("caption", "")
    payload["parse_mode"] = "MarkdownV2"
    payload["caption"] = make_clickable_forwarded_text(original_channel, caption)
    return payload


def process_text_payload(post, forwarded=False):
    text = translate_text(post.get("text", ""))
    payload = {
        "chat_id": TARGET_CHAT_ID,
        "text": text,
        "disable_web_page_preview": True,
    }
    if not forwarded:
        return payload

    original_channel = post.get("forward_origin", {}).get("chat", {}).get("title")
    payload["parse_mode"] = "MarkdownV2"
    payload["text"] = make_clickable_forwarded_text(original_channel, text)
    return payload
