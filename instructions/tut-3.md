# Tutorial 3

## Refactoring to Object-Oriented Programming

In this tutorial, we will refactor our code to use object-oriented programming (OOP) principles by creating a `Transaction` class. We will also learn about code formatting and cleaning up deprecated code. By the end of this tutorial, you will have a cleaner, more maintainable codebase that follows Python best practices.

### Why Refactor?

In Tutorial 2, we implemented functions that worked with transaction dictionaries. However, as our codebase grows, using a proper `Transaction` class provides several benefits:
- **Type safety**: Clear structure for what a transaction contains
- **Encapsulation**: Data and behavior are grouped together
- **Maintainability**: Easier to modify and extend
- **Flexibility**: No longer restricted to predefined transaction types

### Step 1: Check Out the tut-3 Branch ✔

First, ensure you're working on the `tut-3` branch:
```bash
git checkout tut-3
```

### Step 2: Review the Current Code

Open the `transactions.py` file in VSCode. You'll notice:
- A `Transaction` class is already defined at the top
- Several functions with `# TODO` comments that need implementation
- Old functions from Tutorial 2 marked with `# TODO: Remove` comments
- The `TRANSACTION_TYPES` constant marked for removal

The file contains both the old implementation (for reference) and the skeleton for the new implementation.

### Step 3: Clean Up the Old Code

Remove all the deprecated code by deleting the following marked sections:

1. **Remove** the `TRANSACTION_TYPES` constant (around line 7) ✔
2. **Remove** the `add_transaction()` function (marked with TODO) ✔
3. **Remove** the `get_income_total()` function (marked with TODO) ✔
4. **Remove** the `get_expense_total()` function (marked with TODO) ✔
5. **Remove** the `display_transactions()` function (marked with TODO) ✔
6. **Remove** the `if __name__ == "__main__":` block at the end (marked with TODO) ✔

**Tip**: Look for comments that say `#TODO Remove` or `#TODO: Remove` to identify what should be deleted.

### Step 4: Update the calculate_balance Function ✔

The `calculate_balance()` function needs to be updated to work with `Transaction` objects instead of dictionaries:

1. Change the type hint from `List[dict]` to `List[Transaction]`
2. Update the function body to work with Transaction objects using dot notation (e.g., `transaction.amount`)
3. Update the docstring to reflect that it now works with Transaction objects

**Hint**: With the new Transaction class, expenses have negative amounts and income has positive amounts, so you can simply sum all amounts!

### Step 5: Implement the TODO Functions ✔

Now implement the remaining functions marked with `# TODO`:

1. **`calculate_total_expenses()`**: Sum all transactions with negative amounts
2. **`calculate_total_income()`**: Sum all transactions with positive amounts

**Note**: The `format_currency()` function is already implemented—no changes needed.

### Step 6: Format Your Code ✔ ***

Once you've made all changes, format your code using a Python formatter. In the terminal, run:

```bash
black transactions.py
```

If `black` is not installed, install it first:
```bash
pip install black
```

This ensures your code follows PEP 8 style guidelines and looks professional.

### Step 7: Delete the Old Test File ✔

The old test file `test_transactions.py` was designed for the dictionary-based implementation. Delete it:

1. In VSCode, navigate to `tests/test_transactions.py`
2. Right-click the file and select "Delete"
3. Confirm the deletion

### Step 8: Run the New Tests ✔

Now run the new test file designed for the Transaction class:

```bash
pytest tests/test_transaction_class.py
```

This will test your new implementation. All tests should pass if you've implemented everything correctly.

### Step 9: Debug and Fix Issues ✔

If any tests fail:
1. Read the error message carefully
2. Check that you're using dot notation (e.g., `t.amount` not `t['amount']`)
3. Verify that expenses are negative and income is positive
4. Make corrections and run tests again

### Step 10: Commit Your Work ✔

Once all tests pass, commit your refactored code:

1. Check the status of your changes:
   ```bash
   git status
   ```
2. Stage your changes (including the deleted test file):
   ```bash
   git add transactions.py
   git add tests/
   ```
3. Commit with a meaningful message:
   ```bash
   git commit -m "Completed Tutorial 3: Refactor to Transaction class and clean up old code"
   ```
4. Push your changes to the tut-3 branch:
   ```bash
   git push origin tut-3
   ```

---

Congratulations! You have successfully refactored your code to use object-oriented programming principles. This makes your codebase more maintainable, extensible, and follows Python best practices. You are now ready to proceed to Tutorial 4.

Happy coding!