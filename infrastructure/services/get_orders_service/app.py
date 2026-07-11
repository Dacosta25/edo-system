import boto3
import json
import os
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

CORS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type"
}

# Convert DynamoDB Decimals to int/float
def convert_decimal(obj):
    if isinstance(obj, list):
        return [convert_decimal(i) for i in obj]
    if isinstance(obj, dict):
        return {k: convert_decimal(v) for k, v in obj.items()}
    if isinstance(obj, Decimal):
        return int(obj)
    return obj

def lambda_handler(event, context):

    if event.get("httpMethod") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": CORS,
            "body": ""
        }

    try:
        response = table.scan()
        items = response.get("Items", [])

        # Convert all DynamoDB Decimals → ints
        clean_items = convert_decimal(items)

        return {
            "statusCode": 200,
            "headers": CORS,
            "body": json.dumps(clean_items)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": CORS,
            "body": json.dumps({"error": str(e)})
        }