import json
import logging

from app.config.aws_resources import get_ssm_parameter
from app.config.constants import SSM_PARAM_BOT_TOKEN, ALLOWED_CHANNEL_ID
from app.handlers.logic.media_group import handle_media_group
from app.handlers.logic.single_message import handle_single_post
from app.config.env_config import IS_PROD


def setup_logging():
    logging.basicConfig(level=logging.INFO)


setup_logging()
logger = logging.getLogger(__name__)


def is_from_bot(post):
    return post.get("from", {}).get("is_bot") is True


def handler(event, context):
    logger.info("Event received: %s", json.dumps(event))
    BOT_TOKEN = get_ssm_parameter(SSM_PARAM_BOT_TOKEN)
    if IS_PROD:
        path_params = event.get("pathParameters") or {}
        path_param_token = path_params.get("token")
        if path_param_token != BOT_TOKEN:
            logger.warning("Invalid token received: %s", path_param_token)
            return {"statusCode": 403, "body": json.dumps({"message": "Forbidden"})}
        try:
            body = json.loads(event.get("body") or "{}")
            logger.warning("Telegram update: %s", json.dumps(body))
        except json.JSONDecodeError as e:
            logger.error("Failed to decode body: %s", e)
            return {"statusCode": 400, "body": json.dumps({"message": "Invalid JSON"})}
        post = body.get("channel_post", {})
        if is_from_bot(post):
            logger.warning("Nachricht vom Bot selbst – wird ignoriert.")
            return {"statusCode": 200, "body": json.dumps({"message": "Ignored"})}
        if post.get("message_auto_delete_timer_changed"):
            logger.warning(
                "Nachricht über Änderung des Auto-Delete-Timers – wird ignoriert."
            )
            return {"statusCode": 200, "body": json.dumps({"message": "Ignored"})}
        if post.get("chat", {}).get("id") != ALLOWED_CHANNEL_ID:
            logger.warning(post.get("chat", {}).get("id"))
            logger.warning("Erlaubt: %s", ALLOWED_CHANNEL_ID)
            logger.warning("Nicht erlaubter Channel – wird ignoriert.")
            return {"statusCode": 403, "body": json.dumps({"message": "Forbidden"})}
        if "text" not in post and "photo" not in post and "video" not in post:
            logger.info(
                "Ignoriere Systemnachricht oder nicht unterstützten Typ: %s",
                post.keys(),
            )
            return {"statusCode": 200, "body": json.dumps({"message": "Ignored"})}
        media_group_id = post.get("media_group_id")
        forwarded_message = post.get("forward_origin")
    else:
        post = event.get("channel_post", {})
        media_group_id = post.get("media_group_id")
    forwarded = False
    if forwarded_message:
        forwarded = True
        logger.warning("Forwarded message.")
    if media_group_id:
        return handle_media_group(post, media_group_id, BOT_TOKEN, forwarded)
    else:
        return handle_single_post(post, BOT_TOKEN, forwarded)
