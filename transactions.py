from decimal import Decimal, InvalidOperation
from sqlalchemy import Column, ForeignKey, Integer, Numeric, String # SQLAlchemy imports for defining database models and relationships
from sqlalchemy.orm import declarative_base, relationship

from config import Config

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


class Transaction(Base): # Database table called transactions, each instance of this class represents a row in that table
    __tablename__ = "transactions" # Name of the table in the database

    # Mapping of class attributes to database columns
    id = Column(Integer, primary_key=True)
    date = Column(String(32), nullable=False)
    description = Column(String(255), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True) # Foreign key to link to the Category table, can be null if the transaction is uncategorized
    category_ref = relationship("Category", back_populates="transactions") # Establishes a relationship to the Category class, allowing us to access the category of a transaction through the category_ref attribute. The back_populates parameter indicates that the Category class has a corresponding relationship called transactions, which allows us to access all transactions associated with a category.

    def __init__(self, **kwargs): # Custom initializer to ensure amount is always a Decimal
        if "amount" in kwargs: # if amount is provided, try to convert it to Decimal, if it fails raise a ValueError with a clear message
            try:
                kwargs["amount"] = Decimal(kwargs["amount"])
            except (InvalidOperation, ValueError) as e:
                raise ValueError("Amount must be a valid decimal number") from e
        super().__init__(**kwargs)

    def __repr__(self): # What is printed when we print a transaction object
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


def calculate_total_expenses(transactions: list[Transaction]) -> Decimal: # Function to calculate total expenses from a list of transactions that are instances of the Transaction class
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
