import pytest
from decimal import Decimal
from helpers.analysis import generate_text_report
from helpers.transactions import Transaction, Category


@pytest.fixture
def rich_sample_data(db_session):
    """Adds specific data to test all branches of the report logic."""
    # Create required categories
    cat_job = Category(name="Job")
    cat_ent = Category(name="Entertainment")
    cat_house = Category(name="Housing")
    cat_util = Category(name="Utilities")

    db_session.add_all([cat_job, cat_ent, cat_house, cat_util])
    db_session.commit()

    # Add transactions to match your report logic requirements
    txs = [
        # Income
        Transaction(
            date="2024-03-01",
            description="Salary",
            amount=Decimal("20000.00"),
            category_ref=cat_job,
        ),
        # Expenses
        Transaction(
            date="2024-03-01",
            description="Rent",
            amount=Decimal("-5000.00"),
            category_ref=cat_house,
        ),
        # Daily burn over 10 days (approx)
        Transaction(
            date="2024-03-11",
            description="Electricity",
            amount=Decimal("-1000.00"),
            category_ref=cat_util,
        ),
        # Entertainment for % calc
        Transaction(
            date="2024-03-05",
            description="Movie",
            amount=Decimal("-200.00"),
            category_ref=cat_ent,
        ),
    ]

    db_session.add_all(txs)
    db_session.commit()
    return txs


def test_generate_text_report_logic(db_session, rich_sample_data):
    """Tests if the report calculates burn rate, percentages, and coverage correctly."""

    # Act
    report = generate_text_report()

    # Assert - Structure
    assert isinstance(report, dict)
    expected_keys = [
        "Daily Burn Rate",
        "Entertainment %",
        "Essential Coverage",
        "Net Savings",
    ]
    for key in expected_keys:
        assert key in report

    # Assert - Content/Math Checks
    # Total spent = 5000 + 1000 + 200 = 6200
    # Days = (Mar 11 - Mar 1) = 10 days
    # Daily Burn = 6200 / 10 = 620.00
    assert "R 620.00" in report["Daily Burn Rate"]

    # Entertainment % = (200 / 6200) * 100 = ~3.2%
    assert "3.2%" in report["Entertainment %"]

    # Essentials = 5000 + 1000 = 6000. Job = 20000.
    # Ratio = 20000 / 6000 = 3.33 (>= 2 is 'Healthy')
    assert report["Essential Coverage"] == "Healthy"

    # Net Savings = 20000 - 6200 = 13800
    assert "R 13,800.00" in report["Net Savings"]


def test_generate_text_report_empty_db(db_session):
    """Ensures the report handles an empty database gracefully without crashing."""
    # With no data, create_unified_dataframe returns empty DF
    # We want to make sure the division-by-zero checks work
    try:
        report = generate_text_report()
        assert report["Daily Burn Rate"] == "R 0.00"
    except ZeroDivisionError:
        pytest.fail("generate_text_report raised ZeroDivisionError on empty data!")

def test_get_transactions_by_category(db_session, sample_transactions):
    """Tests that transactions are correctly filtered by category."""
    from helpers.analysis import get_transactions_by_category

    groceries_txs = get_transactions_by_category("Groceries")
    assert isinstance(groceries_txs, list)
    assert len(groceries_txs) == 1
    assert groceries_txs[0]["description"] == "PnP Shopping"
    assert groceries_txs[0]["amount"] == "-500.00"

    job_txs = get_transactions_by_category("Job")
    assert len(job_txs) == 2  # Salary and Freelance