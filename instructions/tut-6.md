# Tutorial 6: Project Structure and Data Analysis with Pandas

In this tutorial, we transition from simple data persistence to **Data Analysis**. We have reorganized the project into a professional directory structure and use **Pandas**, the industry-standard library for data manipulation, to derive insights from your financial records.

### Learning Objectives

* Understand the benefits of a modular project structure.
* Learn what **Pandas** is and how it simplifies data aggregation.
* Perform grouped analysis on transactions (e.g., total income vs. total expenses).
* Generate automated reports and visualizations using **Matplotlib**.

---

### Step 1: Check Out the tut-6 Branch ✓

```bash
git checkout tut-6

```

### Step 2: Navigate the New Project Structure ✓

We have moved away from a flat file structure. Your project now looks like this:

* **`data/`**: Contains `database.py` and `seed.py`.
* **`helpers/`**: Contains logic for `transactions.py` and your new analysis tools in `analysis.py`.
* **`static/`**: The destination for generated charts and reports.

### Step 3: What is Pandas?

**Pandas** is a powerful Python library used for data "wrangling." It takes raw data (like your database rows) and puts them into a **DataFrame** - think of it as an Excel spreadsheet on steroids that you can control with code.

In `helpers/analysis.py`, we convert SQLAlchemy results into a DataFrame:

```python
df = pd.DataFrame(results, columns=['name', 'total'])

```

This allows us to perform complex math, like calculating "Burn Rates" or "Savings Ratios," in just one line of code.

### Step 4: Complete the TODOs in `helpers/analysis.py`

Open `helpers/analysis.py` and complete the marked TODOs. There is only one function to implement:
1) `generate_text_report()` – This function should return a formatted string report summarizing total income, total expenses, and net savings. Use Pandas DataFrame methods to calculate these totals efficiently.

Read the comments in the file for guidance on how to use Pandas for these calculations.


### Step 5: Run the App and Generate Charts

You don't need to run the analysis script separately. If you have seeded your database, simply run:

```bash
python app.py

```

`app.py` is already configured to trigger `generate_financial_charts()`. If successful, check your `static/` folder for `expenses_chart.png` and `income_chart.png`.

### Step 6: Run the Tests

We have added a new test suite to verify your Pandas logic. Run:

```bash
pytest tests/test_analysis.py -v

```

This test uses a **pytest fixture**—a pre-populated DataFrame—to ensure your math and filtering logic are 100% accurate.

### Step 7: Commit Your Work

1. **Stage**: Use your editor's Source Control tab to stage `helpers/analysis.py` and `app.py`.
2. **Commit**:
```bash
git commit -m "Completed Tutorial 6: Project reorganization and Pandas analysis"

```



---

### Summary

* **Project Organization**: Moving files into folders like `data/` and `helpers/` makes large projects maintainable.
* **Pandas DataFrames**: These objects make it easy to group, filter, and calculate totals without writing complex SQL or nested `for` loops.
* **Automated Visualization**: By combining Pandas with Matplotlib, we can turn raw database numbers into visual insights automatically.
