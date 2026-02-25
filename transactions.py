from decimal import Decimal, InvalidOperation
from config import Config


CURRENCY_SYMBOL = Config.get_currency_symbol()


class Transaction:
    def __init__(self, date, description, amount, category):
        self.date = date
        self.description = description
        try:
            self.amount = Decimal(amount) # try set amount to be a decimal type. If a person passes in a string that cannot be converted to a decimal, it will raise an InvalidOperation error, which we catch and raise a ValueError with a more user-friendly message.
        except InvalidOperation:
            raise ValueError(f"Invalid amount: {amount}")
        self.category = category

    def __repr__(self):
        return f"Transaction(date='{self.date}', description='{self.description}', amount={format_currency(self.amount)}, category='{self.category}')"


def format_currency(amount=Decimal(0)) -> str:
    """Formats a decimal amount as a Rand (R) string."""
    return f"{CURRENCY_SYMBOL} {amount:.2f}"


def calculate_total_expenses(transactions: list[Transaction]) -> Decimal:
    """Calculates the total expenses from a list of transactions."""
    return sum((t.amount for t in transactions if t.amount < 0), Decimal(0))


def calculate_total_income(transactions: list[Transaction]) -> Decimal:
    """Calculates the total income from a list of transactions."""
    return sum((t.amount for t in transactions if t.amount > 0), Decimal(0))


def calculate_balance(transactions: list[Transaction]) -> Decimal:
    """Calculates the net balance from a list of transactions."""
    return sum((t.amount for t in transactions), Decimal(0))


def check_budget_limit(transactions: list[Transaction], limit: Decimal) -> bool:
    """Checks if the total expenses exceed a given budget limit."""
    total_expenses = calculate_total_expenses(transactions)
    return abs(total_expenses) > limit


#TODO (Hint: This function is called in calculate_financial_summary, check its logic, what if we have no expenses? What if total_expenses is zero?)
def check_financial_health(transactions: list[Transaction]) -> str:
    """Evaluates the financial health based on income and expenses.

    Args:
        transactions (list[Transaction]): List of financial transactions.

    Returns:
        str: A message indicating financial health status, like: "Saving well", or "Overspending".

    """

    total_income = calculate_total_income(transactions)
    total_expenses = abs(calculate_total_expenses(transactions)) 
    
    try:
        health = total_income / (total_expenses)
        if (health >= 1):
            return "Saving well"
        else:
            return "Overspending"
    except (ZeroDivisionError, InvalidOperation):
        if total_income > 0:
            return "Saving well"
        
        return "No transactions recorded."

#TODO Examine this function, it seems to be causing an error in app.py? (Hint: This function uses other functions defined above, it might be related to them)
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
