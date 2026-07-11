"""
Tests for the inventory_worker Lambda.
Covers:
- Successful stock update
- Invalid JSON in record
- Missing fields
- Empty records list
"""

import json
import os
import pytest
from unittest.mock import patch

os.environ["TABLE_NAME"] = "dummy"

from infrastructure.services.inventory_worker.app import handler


@pytest.fixture
def valid_event():
    """Valid SNS→SQS event."""
    return {
        "Records": [
            {"body": json.dumps({"ItemID": "ITEM-001", "Quantity": 5})}
        ]
    }


@patch("infrastructure.services.inventory_worker.app.table.update_item")
def test_inventory_update_success(mock_update, valid_event):
    """Stock update should succeed."""
    mock_update.return_value = True
    response = handler(valid_event, None)
    assert response["statusCode"] == 200


def test_inventory_invalid_json():
    """Invalid JSON should raise JSONDecodeError."""
    event = {"Records": [{"body": "not-json"}]}
    with pytest.raises(json.JSONDecodeError):
        handler(event, None)


def test_inventory_missing_fields():
    """Missing Quantity should raise KeyError."""
    event = {"Records": [{"body": json.dumps({"ItemID": "ITEM-001"})}]}
    with pytest.raises(KeyError):
        handler(event, None)


def test_inventory_no_records():
    """Empty records list should still return 200."""
    event = {"Records": []}
    response = handler(event, None)
    assert response["statusCode"] == 200