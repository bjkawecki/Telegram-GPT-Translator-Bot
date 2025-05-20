import logging

import boto3
from botocore.exceptions import ClientError
from app.config.constants import SSM_OPENAI_KEY_PARAM, DYNAMODB_TABLE_NAME


dynamodb = boto3.resource("dynamodb")
media_group_table = dynamodb.Table(DYNAMODB_TABLE_NAME)
ssm_client = boto3.client("ssm")

logger = logging.getLogger()


def get_ssm_parameter(param_name: str) -> str:
    try:
        response = ssm_client.get_parameter(Name=param_name, WithDecryption=True)
        return response["Parameter"]["Value"]
    except ssm_client.exceptions.ParameterNotFound:
        logger.error(f"Parameter not found: {param_name}")
        raise
    except ClientError as e:
        logger.error(f"Error retrieving parameter {param_name}: {e}")
        raise


openai_api_key = get_ssm_parameter(SSM_OPENAI_KEY_PARAM)
