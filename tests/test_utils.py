"""
Tests for shared/utils.py
Covers:
- validate_order()
- format_response()
"""

import pytest
from shared.utils import validate_order, format_response

def test_validate_order_success():
    """Order with all required fields should pass."""
    order = {"ItemID": "ITEM-001", "Quantity": 5, "CustomerID": "CUST-123"}
    assert validate_order(order) is True

def test_validate_order_missing_fields():
    """Missing fields should raise ValueError."""
    order = {"ItemID": "ITEM-001"}
    with pytest.raises(ValueError):
        validate_order(order)

def test_format_response():
    """format_response should return correct structure."""
    response = format_response(200, {"msg": "ok"})
    assert response["statusCode"] == 200
    assert "ok" in response["body"]