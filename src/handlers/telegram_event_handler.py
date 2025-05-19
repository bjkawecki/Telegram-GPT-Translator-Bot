from src.handlers.logic.media_group import handle_media_group
from src.handlers.logic.single_message import handle_single_post


def handler(event, context):
    post = event.get("channel_post", {})
    media_group_id = post.get("media_group_id")

    if media_group_id:
        return handle_media_group(post, media_group_id)
    else:
        return handle_single_post(post)
