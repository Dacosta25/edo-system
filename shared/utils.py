import json

def parse_sqs_event(event):
    """
    Extracts and yields messages from an SQS event.
    """
    for record in event['Records']:
        body = json.loads(record['body'])
        yield json.loads(body['Message'])


def validate_order(order: dict) -> bool:
    """
    Validates that an order contains all required fields.
    Required fields:
        - ItemID
        - Quantity
        - CustomerID
    Raises:
        ValueError: if any required field is missing.
    """
    required_fields = ["ItemID", "Quantity", "CustomerID"]

    for field in required_fields:
        if field not in order:
            raise ValueError(f"Missing field: {field}")

    return True


def format_response(status_code: int, body: dict) -> dict:
    """
    Formats a standard API Gateway response with JSON body.
    """
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }