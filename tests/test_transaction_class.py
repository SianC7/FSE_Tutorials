import pytest
from decimal import Decimal
from transactions import Transaction, format_currency, calculate_total_expenses, calculate_total_income, calculate_balance, check_financial_health

'''In Pytest, fixtures are functions that create a consistent, repeatable environment or data set for your tests. 
Instead of creating dummy transaction data inside every single test, you define a fixture once and inject it into 
any test that needs it.'''

@pytest.fixture
def sample_transactions():
    return [
        Transaction('2024-01-01', 'Salary', Decimal('10000.00'), 'Income'),
        Transaction('2024-01-02', 'Groceries', Decimal('-500.00'), 'Food'),
        Transaction('2024-01-03', 'Rent', Decimal('-4000.00'), 'Housing'),
        Transaction('2024-01-04', 'Freelance', Decimal('1500.00'), 'Income'),
        Transaction('2024-01-05', 'Dinner', Decimal('-250.50'), 'Food'),
    ]


@pytest.fixture
def income_only_transactions():
    return [
        Transaction('2024-01-01', 'Salary', Decimal('3000.00'), 'Income'),
        Transaction('2024-01-02', 'Bonus', Decimal('500.00'), 'Income'),
    ]

@pytest.fixture
def expenses_only_transactions(): # This fixture provides a list of transactions that only contain expenses, which can be used to test how the system handles scenarios where there is no income, only expenses. T
    return [
        Transaction('2024-01-01', 'Groceries', Decimal('-200.00'), 'Food'),
        Transaction('2024-01-02', 'Rent', Decimal('-800.00'), 'Housing'),
    ]

def test_transaction_creation():
    t = Transaction('2024-01-01', 'Test', '100.00', 'Test Category')
    assert t.date == '2024-01-01'
    assert t.description == 'Test'
    assert t.amount == Decimal('100.00')
    assert t.category == 'Test Category'

def test_invalid_amount():
    with pytest.raises(ValueError):
        Transaction('2024-01-01', 'Invalid', 'abc', 'Error')

def test_format_currency():
    assert format_currency(Decimal('123.456')) == 'R 123.46'
    assert format_currency(Decimal('-50.00')) == 'R -50.00'

def test_calculate_total_expenses(sample_transactions):
    assert calculate_total_expenses(sample_transactions) == Decimal('-4750.50')

def test_calculate_total_income(sample_transactions):
    assert calculate_total_income(sample_transactions) == Decimal('11500.00')

def test_calculate_balance(sample_transactions):
    assert calculate_balance(sample_transactions) == Decimal('6749.50')

#NOTE This is an example of a test, you should add more tests to cover different scenarios
def test_empty_transactions():
    empty_list = []
    assert calculate_total_expenses(empty_list) == Decimal('0')
    assert calculate_total_income(empty_list) == Decimal('0')
    assert calculate_balance(empty_list) == Decimal('0')
    assert check_financial_health(empty_list) == "No transactions recorded." # Since income is 0

#TODO Complete this test
def test_only_expenses(expenses_only_transactions):
    assert calculate_total_income(expenses_only_transactions) == Decimal('0')
    assert calculate_total_expenses(expenses_only_transactions) == Decimal('-1000.00')
    assert calculate_balance(expenses_only_transactions) == Decimal('-1000.00')
    assert check_financial_health(expenses_only_transactions) == "Overspending" # Since income is 0 and expenses are negative, we are overspending
    pass

#TODO Complete this test
def test_only_income(income_only_transactions):
    assert calculate_total_income(income_only_transactions) == Decimal('3500.00')
    assert calculate_total_expenses(income_only_transactions) == Decimal('0')
    assert calculate_balance(income_only_transactions) == Decimal('3500.00')
    assert check_financial_health(income_only_transactions) == "Saving well" # Since we have income and no expenses, we are saving well
    pass

#TODO Complete this test
def test_mixed_transactions(sample_transactions):
    assert calculate_total_income(sample_transactions) == Decimal('11500.00')
    assert calculate_total_expenses(sample_transactions) == Decimal('-4750.50')
    assert calculate_balance(sample_transactions) == Decimal('6749.50')
    assert check_financial_health(sample_transactions) == "Saving well" # Since we have more
    pass
