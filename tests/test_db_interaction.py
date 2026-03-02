from decimal import Decimal

from sqlalchemy import select

from app import (
    add_entertainment_category,
    add_entertainment_expenses,
    display_transactions_by_category,
)
from transactions import Category, Transaction


def test_add_entertainment_category_creates_and_reuses(db_session):
    add_entertainment_category()
    add_entertainment_category()  # idempotent

    categories = select(Category).where(Category.name == "Entertainment")
    categories = db_session.execute(categories).scalars().all()
    assert len(categories) == 1


def test_add_entertainment_expenses_inserts_sample_data(db_session):
    add_entertainment_category()
    add_entertainment_expenses()
    # Build statement
    stmt = select(Transaction).filter(Transaction.amount < 0)
    # Execute and fetch results
    expenses = db_session.execute(stmt).scalars().all()
    assert len(expenses) == 2
    assert all(exp.category_id is not None for exp in expenses)


def test_display_transactions_by_category_outputs(capsys, db_session):
    income = Category(name="Income")
    db_session.add(income)
    db_session.add(
        Transaction(
            date="2024-02-01",
            description="Salary",
            amount=Decimal("5000"),
            category_ref=income,
        )
    )
    db_session.commit()

    display_transactions_by_category("Income")
    captured = capsys.readouterr().out

    # assert "Transactions in category 'Income':" in captured
    assert "Salary" in captured
