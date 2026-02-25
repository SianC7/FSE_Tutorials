# Tutorial 4

## Environment Variables, Error Handling & Testing

In this tutorial, you will learn how to work with environment variables, debug runtime errors, and write comprehensive unit tests. By the end of this tutorial, you will understand how to configure applications securely, handle exceptions gracefully, and test different scenarios thoroughly.

### Learning Objectives

- Load and use environment variables with `python-dotenv`
- Identify and fix division by zero errors
- Implement try-except blocks for error handling
- Write unit tests for different transaction scenarios
- Understand how pytest works and how to test functions

### Step 1: Check Out the tut-4 Branch ✓

First, ensure you're working on the `tut-4` branch:
```bash
git checkout tut-4
```

## Part 1: Environment Variables

### Step 2: Understanding Environment Variables

Environment variables are key-value pairs stored outside your code. They're used to store:
- Secrets (API keys, passwords, database credentials)
- Configuration values that change between environments (development, production)
- Settings that shouldn't be hardcoded

In our project, we use environment variables to store:
- `SECRET_KEY`: A secret key for security features
- `CURRENCY_SYMBOL`: The currency symbol to display (e.g., "R" for Rand)

### Step 3: Create Your .env File ✓

1. In the root directory of the project, you'll find a `.env.example` file
2. Create a new file named `.env` in the same directory
3. Copy the contents from `.env.example` into your new `.env` file:

```dotenv
SECRET_KEY=supersecretkey
CURRENCY_SYMBOL=R
```

**Important**: The `.env` file should never be committed to git (it's already in `.gitignore`). The `.env.example` file shows what variables are needed without exposing actual secrets.

### Step 4: Load Environment Variables in config.py ✓

Open the `config.py` file. You'll see it currently has hardcoded values:

```python
class Config:
    SECRET_KEY = "notsosecret"
    CURRENCY_SYMBOL = "$"
```

Your task is to load these values from the `.env` file instead. Replace the hardcoded values with:

```python
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")
    CURRENCY_SYMBOL = os.getenv("CURRENCY_SYMBOL", "$")
```

**What this does**:
- `os.getenv("SECRET_KEY", "default_secret")` reads the `SECRET_KEY` from environment variables
- The second parameter (`"default_secret"`) is the default value if the variable isn't found
- The `load_dotenv()` at the top of the file loads variables from `.env`

### Step 5: Test the Configuration ✓

Run the configuration tests to verify your environment variables are loaded correctly:

```bash
pytest tests/test_config.py
```

If successful, you should see both tests pass!

## Part 2: Error Handling

### Step 6: Run the Application

Now let's try running the main application:

```bash
python app.py
```

**Uh oh!** You should see an error. This is intentional—let's learn how to debug it!

### Step 7: Investigate the Error ✓

The error message will show something like `ZeroDivisionError: division by zero`. Let's trace it:

1. Look at the error traceback—it tells you which line caused the error
2. The error originates in `calculate_financial_summary()` in `transactions.py`
3. This function calls `check_financial_health()`
4. Inside `check_financial_health()`, there's a division operation

**Can you spot the problem?**

Look at this line in `check_financial_health()`:
```python
health = total_income / (total_expenses)
```

**The Problem**: In `app.py`, the sample transactions only have income, no expenses! So `total_expenses` is zero, causing a division by zero error.

### Step 8: Understanding the Logic ✓

The `check_financial_health()` function evaluates financial health by dividing income by expenses. But what happens when:
- There are no expenses? (division by zero)
- There's no income? (can't determine health)
- Both are zero? (no transactions)

We need to handle these edge cases!

### Step 9: Fix the Error with Try-Except ✓

Add a try-except block to handle the division by zero error. Update the `check_financial_health()` function:

```python
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
    except ZeroDivisionError:
        # Handle the case when there are no expenses
        if total_income > 0:
            return "No expenses recorded"
        else:
            return "No transactions recorded"
```

**What this does**:
- The `try` block attempts the division
- If a `ZeroDivisionError` occurs, the `except` block handles it
- We return meaningful messages based on whether there's income

### Step 10: Test the Fix ✓

Now run the application again:
```bash
python app.py
```

It should work! You'll see a financial summary with "No expenses recorded" as the health status.

### Step 11: Uncomment the Expense Transaction ✓

In `app.py`, uncomment line 11 to add an expense transaction:
```python
Transaction(description="Gift", amount=Decimal("-2000"), category="expense", date=datetime.now()),
```

Run the application again:
```bash
python app.py
```

Now you should see "Saving well" as the health status since income exceeds expenses!

## Part 3: Writing Unit Tests

### Step 12: Understanding Unit Tests

Unit tests verify that individual functions work correctly. Let's understand the structure of a test:

```python
def test_calculate_total_income(sample_transactions):
    assert calculate_total_income(sample_transactions) == Decimal('11500.00')
```

**Breaking it down**:
- `def test_...`: Test functions must start with `test_`
- `sample_transactions`: A **fixture** that provides test data (defined at the top of the file)
- `assert`: Checks if the condition is true; if false, the test fails
- The test calls the function and verifies the output matches what we expect

### Step 13: Understanding Fixtures

Look at the top of `test_transaction_class.py` inside the `tests` folder. You'll see fixtures like:

```python
@pytest.fixture
def sample_transactions():
    return [
        Transaction('2024-01-01', 'Salary', Decimal('10000.00'), 'Income'),
        Transaction('2024-01-02', 'Groceries', Decimal('-500.00'), 'Food'),
        ...
    ]
```

**Fixtures** are reusable test data:
- They're defined once and can be used by multiple tests
- Pytest automatically passes them to test functions that request them
- They help keep tests clean and avoid duplication

### Step 14: Complete the Test Cases

Now it's your turn! Complete the three TODO test cases in `test_transaction_class.py`, I have provided a test for empty transactions as an example.

#### Test 1: test_only_expenses

Test the functions when there are only expense transactions:

**What we're testing**:
- Income should be zero
- Expenses should sum to -1000.00 (-200 + -800)
- Balance should equal expenses (negative)
- Financial health should show "Overspending" (no income to cover expenses)

#### Test 2: test_only_income

Test the functions when there are only income transactions:

**What we're testing**:
- Expenses should be zero
- Income should sum to 3500.00 (3000 + 500)
- Balance should equal income (positive)
- Financial health should show "No expenses recorded" (handled by our try-except!)

#### Test 3: test_mixed_transactions

Test the functions with a mix of income and expenses:

**What we're testing**:
- Income is 11,500 (10,000 + 1,500)
- Expenses are -4,750.50 (-500 + -4,000 + -250.50)
- Balance is 6,749.50 (11,500 - 4,750.50)
- Financial health shows "Saving well" (income exceeds expenses)

### Step 15: Run All Tests

Once you've completed the test cases, run all tests:

```bash
pytest .\tests -v
```

The `-v` flag (verbose) shows detailed output for each test. All tests should pass!

### Step 16: Understanding Test Output

When tests pass, you'll see:
```
test_transaction_creation PASSED
test_only_expenses PASSED
...
```

If a test fails, you'll see:
- Which test failed
- The assertion that failed
- Expected vs actual values

This helps you quickly identify and fix issues!

## Step 17: Commit Your Work

Once all tests pass, commit your completed work:

1. Check the status of your changes:
   ```bash
   git status
   ```

2. Stage your changes:
   ```bash
   git add config.py
   git add .env
   git add transactions.py
   git add app.py
   git add tests/test_transaction_class.py
   ```

3. Commit with a meaningful message:
   ```bash
   git commit -m "Completed Tutorial 4: Environment variables, error handling, and comprehensive testing"
   ```

4. Push your changes to the tut-4 branch:
   ```bash
   git push origin tut-4
   ```

---

## Summary

Congratulations! In this tutorial, you learned:

- **Environment Variables**: How to use `.env` files to store configuration securely  
- **Error Handling**: How to use try-except blocks to handle runtime errors gracefully  
- **Debugging**: How to read error messages and trace issues to their source  
- **Unit Testing**: How to write comprehensive tests for different scenarios  
- **Pytest**: How fixtures work and how to verify function behavior

These are essential software engineering skills that you'll use throughout your career!

Happy coding!
