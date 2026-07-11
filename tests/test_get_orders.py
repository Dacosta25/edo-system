"""
Tests for the ingestion_service Lambda.
Covers:
- OPTIONS preflight
- JSON validation
- Missing fields
- DynamoDB write failures
- SNS publish failures
- Successful order creation
"""

import json
import os
from unittest.mock import patch, MagicMock
import pytest

# Environment variables required by the Lambda
os.environ["ORDERS_TABLE"] = "dummy"
os.environ["TOPIC_ARN"] = "dummy"

# Import the Lambda handler
from infrastructure.services.ingestion_service.app import handler


# Fake context object to simulate AWS Lambda context
class FakeContext:
    aws_request_id = "abc-123"


# A valid POST event used in multiple tests
@pytest.fixture
def valid_event():
    return {
        "httpMethod": "POST",
        "body": json.dumps({
            "ItemID": "ITEM-001",
            "Quantity": 3,
            "CustomerID": "CUST-999"
        })
    }


def test_options_preflight():
    """OPTIONS request should return 200 with empty body."""
    event = {"httpMethod": "OPTIONS"}
    response = handler(event, None)
    assert response["statusCode"] == 200
    assert response["body"] == ""


def test_invalid_json():
    """Invalid JSON should return a 400 error."""
    event = {"httpMethod": "POST", "body": "not-json"}
    response = handler(event, None)
    assert response["statusCode"] == 400


def test_missing_fields():
    """Missing required fields should return a 400 error."""
    event = {"httpMethod": "POST", "body": json.dumps({"ItemID": "ITEM-001"})}
    response = handler(event, None)
    assert response["statusCode"] == 400


@patch("infrastructure.services.ingestion_service.app.ORDERS_TABLE.put_item")
def test_dynamodb_failure(mock_put, valid_event):
    """Simulate DynamoDB write failure."""
    mock_put.side_effect = Exception("DynamoDB error")
    response = handler(valid_event, FakeContext())
    assert response["statusCode"] == 500


@patch("infrastructure.services.ingestion_service.app.ORDERS_TABLE.put_item")
@patch("infrastructure.services.ingestion_service.app.sns.publish")
def test_sns_failure(mock_publish, mock_put, valid_event):
    """Simulate SNS publish failure."""
    mock_put.return_value = True
    mock_publish.side_effect = Exception("SNS error")
    response = handler(valid_event, FakeContext())
    assert response["statusCode"] == 500


@patch("infrastructure.services.ingestion_service.app.ORDERS_TABLE.put_item")
@patch("infrastructure.services.ingestion_service.app.sns.publish")
def test_successful_order(mock_publish, mock_put, valid_event):
    """Successful order should return 200."""
    mock_put.return_value = True
    mock_publish.return_value = True
    response = handler(valid_event, FakeContext())
    assert response["statusCode"] == 200