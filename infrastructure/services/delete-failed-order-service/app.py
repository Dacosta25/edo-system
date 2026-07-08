import json
import boto3
import os

sqs = boto3.client("sqs")
DLQ_URL = os.environ["DLQ_URL"]

def handler(event, context):
    receipt_handle = event["pathParameters"]["receiptHandle"]

    sqs.delete_message(
        QueueUrl=DLQ_URL,
        ReceiptHandle=receipt_handle
    )

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "DELETE,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": json.dumps({"message": "Deleted"})
    }
