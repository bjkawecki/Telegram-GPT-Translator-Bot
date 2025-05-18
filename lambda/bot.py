import boto3
import json


SSM_PARAM_BOT_TOKEN = "/mirrowchan_bot/bot_token"
ssm = boto3.client("ssm")


def get_webhook_token(ssm_param_bot_token):
    response = ssm.get_parameter(Name=ssm_param_bot_token, WithDecryption=True)
    return response["Parameter"]["Value"]


def handler(event, context):
    # 1. Bot-Token zur Verifikation
    expected_token = get_webhook_token(SSM_PARAM_BOT_TOKEN)
    print("expected_token:", expected_token)
    # 2. Extract path parameter {token} from API Gateway event
    path_params = event.get("pathParameters", {})
    received_token = path_params.get("token")
    if received_token != expected_token:
        return {"statusCode": 403, "body": json.dumps({"message": "Forbidden"})}

    # 3. Telegram Webhook Payload
    body = json.loads(event.get("body", "{}"))
    print(f"Received Telegram update: {body}")
    return {"statusCode": 200, "body": json.dumps({"message": "OK"})}
