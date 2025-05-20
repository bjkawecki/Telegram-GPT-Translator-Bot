import re


def escape_markdown(text: str) -> str:
    escape_chars = r"_*\[\]()~`>#+-=|{}.!"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)


def make_clickable_forwarded_text(original_channel: str, text: str) -> str:
    escaped_text = escape_markdown(text)
    escaped_channel = escape_markdown(original_channel)
    return f"*[🔁 Weitergeleitet aus {escaped_channel}](https://t.me/{original_channel})*\n\n{escaped_text}"
