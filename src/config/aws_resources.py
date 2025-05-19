import boto3

dynamodb = boto3.resource("dynamodb")
media_group_table = dynamodb.Table("MediaGroupBuffer")
