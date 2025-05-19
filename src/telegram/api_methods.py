from src.config.env_config import BOT_TOKEN


def select_send_method(post_type):
    send_method_config = {
        "text": "sendMessage",
        "photo": "sendPhoto",
        "video": "sendVideo",
        "media_group": "sendMediaGroup",
    }
    return send_method_config.get(post_type)


def prepare_url(api_send_method):
    return f"https://api.telegram.org/bot{BOT_TOKEN}/{api_send_method}"
