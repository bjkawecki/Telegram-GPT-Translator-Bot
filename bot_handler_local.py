import json

import boto3

ssm = boto3.client("ssm")

SSM_PARAM_BOT_TOKEN = "/mirrowchan_bot/bot_token"
SSM_PARAM_WEBHOOK_URL = "/mirrowchan_bot/api_gateway_url"


def get_value_from_ssm(parameter_name):
    ssm = boto3.client("ssm")
    response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
    return response["Parameter"]["Value"]


def handler(event, context):
    # 1. Bot-Token zur Verifikation
    expected_token = get_value_from_ssm(SSM_PARAM_BOT_TOKEN)
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


if __name__ == "__main__":
    # Beispiel-Ereignis, wie es von API Gateway oder EventBridge kommen könnte
    test_event = {"key1": "value1", "key2": "value2"}
    # Du kannst 'context' weglassen oder ein Mock-Objekt übergeben
    result = handler(test_event, context=None)

    print("Lambda result:", result)
