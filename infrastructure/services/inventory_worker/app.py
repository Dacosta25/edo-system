import json
import boto3
import os
from shared.logging import log_info

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def handler(event, context):
    log_info("Worker received event", event)

    for record in event["Records"]:
        # Raw SNS → SQS delivery: body contains the actual message
        sns_message = json.loads(record["body"])

        item_id = sns_message["ItemID"]
        quantity = sns_message["Quantity"]

        log_info("Updating stock", {"ItemID": item_id, "Quantity": quantity})

        table.update_item(
            Key={"ItemID": item_id},
            UpdateExpression="SET Stock = if_not_exists(Stock, :zero) - :val",
            ExpressionAttributeValues={
                ":val": quantity,
                ":zero": 0
            }
        )

    return {"statusCode": 200, "body": "Inventory updated"}