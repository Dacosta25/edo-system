import json
import boto3
import os
from shared.logging import log_info

sns = boto3.client("sns")
dynamodb = boto3.resource("dynamodb")

TOPIC_ARN = os.environ["TOPIC_ARN"]
ORDERS_TABLE = dynamodb.Table(os.environ["ORDERS_TABLE"])

# CORS headers for ALL responses
CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,POST"
}

def handler(event, context):
    log_info("Received event", event)

    # 0. Handle OPTIONS preflight request
    if event.get("httpMethod") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": CORS_HEADERS,
            "body": ""
        }

    # 1. Parse body
    try:
        body = json.loads(event.get("body", "{}"))
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": "Invalid JSON"})
        }

    # 2. Validate fields
    if "ItemID" not in body or "Quantity" not in body or "CustomerID" not in body:
        return {
            "statusCode": 400,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": "ItemID, Quantity, and CustomerID are required"})
        }

    # 3. Generate OrderID
    order_id = f"order-{context.aws_request_id}"
    body["OrderID"] = order_id

    # 4. Write order to DynamoDB (OrdersTable)
    try:
        ORDERS_TABLE.put_item(Item=body)
        log_info("Order written to DynamoDB", body)
    except Exception as e:
        log_info("DynamoDB write failed", str(e))
        return {
            "statusCode": 500,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": "Failed to write order to database"})
        }

    # 5. Publish to SNS (for inventory worker)
    try:
        sns.publish(
            TopicArn=TOPIC_ARN,
            Message=json.dumps(body)
        )
        log_info("Published to SNS", body)
    except Exception as e:
        log_info("SNS publish failed", str(e))
        return {
            "statusCode": 500,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": "Failed to publish message"})
        }

    # 6. Success response
    return {
        "statusCode": 200,
        "headers": CORS_HEADERS,
        "body": json.dumps({
            "message": "Order accepted and routing in progress",
            "OrderID": order_id
        })
    }
