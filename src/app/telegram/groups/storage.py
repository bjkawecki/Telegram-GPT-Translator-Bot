import time
from boto3.dynamodb.conditions import Key
from app.config.aws_resources import media_group_table


def store_media_group_item(media_group_id, message_id, post, ttl_seconds=1):
    """Speichert ein MediaGroup-Element mit optionalem TTL (Default: 60s)."""
    print(f"==> Speichere in DynamoDB: {media_group_id=}, {message_id=}")
    expires_at = int(time.time()) + ttl_seconds
    media_group_table.put_item(
        Item={
            "media_group_id": media_group_id,
            "message_id": message_id,
            "post": post,
            "expires_at": expires_at,
        }
    )


def get_media_group(media_group_id):
    """Holt alle Nachrichten einer MediaGroup aus DynamoDB, sortiert nach message_id."""
    response = media_group_table.query(
        KeyConditionExpression=Key("media_group_id").eq(media_group_id)
    )
    items = response.get("Items", [])
    return sorted(items, key=lambda x: x["message_id"])


def delete_media_group(media_group_id):
    """Löscht alle zugehörigen Nachrichten einer MediaGroup aus der DB."""
    items = get_media_group(media_group_id)
    with media_group_table.batch_writer() as batch:
        for item in items:
            batch.delete_item(
                Key={
                    "media_group_id": media_group_id,
                    "message_id": item["message_id"],
                }
            )
