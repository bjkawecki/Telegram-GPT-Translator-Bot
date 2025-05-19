import logging

import boto3

dynamodb = boto3.resource("dynamodb")
media_group_table = dynamodb.Table("MediaGroupBuffer")
ssm = boto3.client("ssm")


logger = logging.getLogger()


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
