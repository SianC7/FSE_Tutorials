import pytest
from decimal import Decimal
from unittest.mock import patch

from app import app
from helpers.transactions import Transaction


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# def test_financial_summary_endpoint(client):
#     """Test that /api/financial_summary returns the correct text report."""
#     response = client.get("/api/financial_summary")
    
#     assert response.status_code == 200
#     assert response.is_json

#     data = response.get_json()
#     assert "Daily Burn Rate" in data
#     assert "Entertainment %" in data
#     assert "Essential Coverage" in data
#     assert "Net Savings" in data


def test_financial_charts_endpoint(client):
    """Test that /api/financial_charts returns chart paths."""
    mock_charts = {
        "expenses": "/path/to/expenses_pie.png",
        "income": "/path/to/income_pie.png",
    }

    with patch("app.generate_financial_charts", return_value=mock_charts):
        response = client.get("/api/financial_charts")

        assert response.status_code == 200
        assert response.is_json

        data = response.get_json()
        assert "expenses" in data
        assert "income" in data
        assert data["expenses"] == "/static/expenses_pie.png"
        assert data["income"] == "/static/income_pie.png"


def test_transactions_by_category_endpoint(client, sample_transactions):
    """Test that /api/transactions returns filtered transactions by category."""
    response = client.get("/api/transactions?category=Groceries")
    assert response.status_code == 200
    assert response.is_json

    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["category"] == "Groceries"
    assert data[0]["description"] == "PnP Shopping"
