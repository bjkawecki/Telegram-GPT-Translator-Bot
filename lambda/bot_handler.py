import boto3
import json

ssm = boto3.client("ssm")


def get_webhook_token():
    response = ssm.get_parameter(
        Name="/mirrowchan_bot/webhook_token", WithDecryption=True
    )
    return response["Parameter"]["Value"]


def handler(event, context):
    # 1. Bot-Token zur Verifikation
    expected_token = get_webhook_token()
    # 2. Extract path parameter {token} from API Gateway event
    path_params = event.get("pathParameters", {})
    received_token = path_params.get("token")

    if received_token != expected_token:
        return {"statusCode": 403, "body": json.dumps({"message": "Forbidden"})}

    # 3. Telegram Webhook Payload
    body = json.loads(event.get("body", "{}"))
    print(f"Received Telegram update: {body}")

    # 4. Hier geht's dann mit deiner Logik weiter
    # z.B. OpenAI API Aufruf & Antwort in Spiegel-Kanal posten

    return {"statusCode": 200, "body": json.dumps({"message": "OK"})}
