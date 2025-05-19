import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

SSM_PARAM_BOT_TOKEN = "/mirrowchan_bot/bot_token"

ssm = boto3.client("ssm")


def get_webhook_token(param_name: str) -> str:
    try:
        response = ssm.get_parameter(Name=param_name, WithDecryption=True)
        return response["Parameter"]["Value"]
    except ssm.exceptions.ParameterNotFound:
        logger.error(f"Parameter not found: {param_name}")
        raise
    except Exception as e:
        logger.error(f"Error retrieving parameter {param_name}: {e}")
        raise


def handler(event, context):
    logger.info("Event received: %s", json.dumps(event))

    expected_token = get_webhook_token(SSM_PARAM_BOT_TOKEN)

    path_params = event.get("pathParameters") or {}
    received_token = path_params.get("token")

    if received_token != expected_token:
        logger.warning("Invalid token received: %s", received_token)
        return {"statusCode": 403, "body": json.dumps({"message": "Forbidden"})}

    try:
        body = json.loads(event.get("body") or "{}")
        logger.info("Telegram update: %s", json.dumps(body))
    except json.JSONDecodeError as e:
        logger.error("Failed to decode body: %s", e)
        return {"statusCode": 400, "body": json.dumps({"message": "Invalid JSON"})}

    return {"statusCode": 200, "body": json.dumps({"message": "OK"})}
