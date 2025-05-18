import boto3

import requests


SSM_PARAM_BOT_TOKEN = "/mirrowchan_bot/bot_token"
SSM_PARAM_WEBHOOK_URL = "/mirrowchan_bot/api_gateway_url"


def get_value_from_ssm(parameter_name):
    ssm = boto3.client("ssm")
    response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
    return response["Parameter"]["Value"]


def set_webhook(bot_token, webhook_url):
    if not bot_token or not webhook_url:
        print("BOT_TOKEN oder WEBHOOK_URL fehlt.")
        return

    url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
    webhook_url = webhook_url + "/webhook/" + bot_token
    response = requests.post(url, data={"url": webhook_url})

    if response.ok:
        print("Webhook erfolgreich gesetzt!")
        print("Antwort:", response.json())
    else:
        print("Fehler beim Setzen des Webhooks:")
        print(response.text)


if __name__ == "__main__":
    try:
        bot_token = get_value_from_ssm(SSM_PARAM_BOT_TOKEN)
        webhook_url = get_value_from_ssm(SSM_PARAM_WEBHOOK_URL)
        set_webhook(bot_token, webhook_url)

    except Exception as e:
        print(f"Fehler beim Abrufen der URL oder Setzen des Webhooks: {e}")
