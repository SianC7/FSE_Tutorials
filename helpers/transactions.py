from decimal import Decimal, InvalidOperation
from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import declarative_base, relationship

from helpers.config import Config

CURRENCY_SYMBOL = Config.get_currency_symbol()
Base = declarative_base()


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    transactions = relationship(
        "Transaction",
        back_populates="category_ref",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"Category(id={self.id}, name='{self.name}')"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    date = Column(String(32), nullable=False)
    description = Column(String(255), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    category_ref = relationship("Category", back_populates="transactions")

    def __init__(self, **kwargs):
        if "amount" in kwargs:
            try:
                kwargs["amount"] = Decimal(kwargs["amount"])
            except (InvalidOperation, ValueError) as e:
                raise ValueError("Amount must be a valid decimal number") from e
        super().__init__(**kwargs)

    def __repr__(self):
        amt = Decimal(str(self.amount)) if self.amount is not None else Decimal("0.00")
        return (
            "Transaction("
            f"id={self.id}, date='{self.date}', description='{self.description}', "
            f"amount={format_currency(amt)}, category='{self.category_ref.name if self.category_ref else None}', "
            f"category_id={self.category_id})"
        )


def format_currency(amount: Decimal) -> str:
    """Formats a decimal amount as a Rand (R) string."""
    return f"{CURRENCY_SYMBOL} {amount:.2f}"


def calculate_total_expenses(transactions: list[Transaction]) -> Decimal:
    """Calculates the total expenses from a list of transactions."""
    return sum(
        (Decimal(str(t.amount)) for t in transactions if Decimal(str(t.amount)) < 0),
        Decimal(0),
    )


def calculate_total_income(transactions: list[Transaction]) -> Decimal:
    """Calculates the total income from a list of transactions."""
    return sum(
        (Decimal(str(t.amount)) for t in transactions if Decimal(str(t.amount)) > 0),
        Decimal(0),
    )


def calculate_balance(transactions: list[Transaction]) -> Decimal:
    """Calculates the net balance from a list of transactions."""
    return sum((Decimal(str(t.amount)) for t in transactions), Decimal(0))


def check_budget_limit(transactions: list[Transaction], limit: Decimal) -> bool:
    """Checks if the total expenses exceed a given budget limit."""
    total_expenses = calculate_total_expenses(transactions)
    return abs(total_expenses) > limit


def check_financial_health(transactions: list[Transaction]) -> str:
    """Evaluates the financial health based on income and expenses."""
    total_income = calculate_total_income(transactions)
    total_expenses = abs(calculate_total_expenses(transactions))

    try:
        health = total_income / total_expenses
        if health >= 1:
            return "Saving well"
        else:
            return "Overspending"
    except (ZeroDivisionError, InvalidOperation):
        # Handle the case when there are no expenses
        if total_income > 0:
            return "No expenses recorded"
        else:
            return "No transactions recorded"


def calculate_financial_summary(transactions: list[Transaction]) -> dict:
    """Calculates a financial summary including total income, expenses, balance and financial health."""
    total_income = calculate_total_income(transactions)
    total_expenses = calculate_total_expenses(transactions)
    balance = calculate_balance(transactions)
    health = check_financial_health(transactions)
    return {
        "total_income": format_currency(total_income),
        "total_expenses": format_currency(total_expenses),
        "balance": format_currency(balance),
        "financial_health": health,
    }
