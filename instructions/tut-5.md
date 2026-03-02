# Tutorial 5

## ORMs, Sessions, and Using the Database

In this tutorial, you will move from in-memory objects to working with a relational database through SQLAlchemy's ORM. The models (schemas) are already defined for you; your job is to wire up sessions, run the supplied helpers, and complete the TODOs in `app.py` so that categories and transactions persist and can be queried.

### Learning Objectives

- Understand what an ORM is and why we map Python classes to database tables
- Use SQLAlchemy's `engine`, `Session`, and `declarative_base`
- Create and reuse categories and transactions via ORM sessions
- Run and extend the provided database helpers in `app.py`
- Validate your work with automated tests

### Step 1: Check Out the tut-5 Branch ✔

```bash
git checkout tut-5 
```

### Step 2: Refresh ORM Concepts ✔

An **Object-Relational Mapper (ORM)** lets you work with database rows as Python objects instead of raw SQL. In this project:
- `Category` ↔ `categories` table
- `Transaction` ↔ `transactions` table, with a `category_id` foreign key and a `category_ref` relationship

Open `transactions.py` and skim the models to see how columns and relationships are declared. You do **not** need to change these models for this tutorial.

### Step 3: Configure the Database URL ✔

`config.py` exposes `Config.get_database_url()`. By default it uses SQLite:

```
sqlite:///finance.db
```

If you want to use a different database, set `DATABASE_URL` in your `.env`, then reload the shell or IDE.

### Step 4: Initialize the Database

`database.py` provides:
- `init_db()` – creates tables for all models
- `get_session()` – returns a SQLAlchemy session bound to the configured engine

Run the seed script once to populate baseline data (income + expenses):

```bash
python seed.py
```

### Step 5: Complete the TODOs in app.py

Open `app.py` and finish the marked TODOs. The intent of each helper:

1) `add_entertainment_category()` – ensure an `Entertainment` category exists (create it if missing, otherwise reuse it).

2) `add_entertainment_expenses()` – insert sample negative expenses (e.g., Groceries, Utilities) under the `Entertainment` category.

3) `display_transactions_by_category(category_name)` – query and print all transactions for a given category name. Use the ORM query API (no raw SQL needed).

After implementing, run the app to see the summary and category listings:

```bash
python app.py
```

### Step 6: Interact with Sessions

Remember the typical session pattern:

```python
from database import get_session

session = get_session()
try:
	# add/query objects
	session.add(obj)
	session.commit()
finally:
	session.close()
```

- Call `commit()` after inserts/updates to persist changes.
- Use `filter_by(...)` or `filter(...)` to query.
- Always `close()` sessions in a `finally` block.

### Step 7: Run the Tests

Two test suites validate your work:

- Transaction calculations: `pytest tests/test_transaction_class.py -v`
- Database interactions and TODOs: `pytest tests/test_db_interaction.py -v`

Run both and ensure all tests pass:

```bash
pytest ./tests/ -v
```
All tests should pass when the TODOs are correctly implemented and the ORM helpers behave as expected.


### Step 8: Commit Your Work
Once all tests pass, commit your completed work:
1. Check the status of your changes:
   ```bash
   git status
   ```

2. Stage your changes:
For this tutorial, we are going to use your editors built in source control management to stage and commit your changes.

3. Commit with a meaningful message:
   ```bash
   git commit -m "Completed Tutorial 5: ORM integration with SQLAlchemy"
   ```


### Summary

- ORMs map Python classes to tables, letting you work with objects instead of SQL strings
- Sessions manage database conversations: open, add/query, commit, close
- Relationships (foreign keys + backrefs) let you navigate linked data naturally
- Writing a few helper functions plus tests is enough to exercise the ORM without redefining schemas

Happy coding!
