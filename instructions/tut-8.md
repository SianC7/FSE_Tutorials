# Tutorial 8: Rendering Data with Jinja2 Templates

In this tutorial you will finish the main dashboard by wiring dynamic data into the HTML template. You will learn what a **template** is, how **Jinja2** renders values, and how to complete the TODOs for two new metric cards on the page.

Previously, we built the API logic as an example of how we might serve a real customer frontend. Now we will build our own frontend directly into `app.py` using Flask's templating system.

You can still visit the customer dashboard by going to `http://localhost:5000/customer` after running `app.py`, but now we will focus on the main dashboard at `http://localhost:5000/`.

### Learning Objectives

- Understand what a template is and how Jinja2 replaces placeholders with real data.
- Pass data from a Flask view into a template using `render_template`.
- Use Jinja2 expressions (`{{ ... }}`) and conditionals (`{% if ... %}`) in HTML.
- Implement two dashboard cards (Largest Expense and Average Transaction) by completing TODOs in `app.py` and `templates/dashboard.html`.

---

## What is a Template? ✓
A **template** is an HTML file with placeholders for data. Flask uses **Jinja2** to fill those placeholders at render time. **Jinja2** allows us to put python code in html files. The flow is:
1. Flask view prepares data (Python dicts, lists, objects).
2. `render_template` sends that data into a `.html` template.
3. Jinja2 swaps `{{ variables }}` and executes `{% logic %}` blocks to produce final HTML.


You’ll commonly use:
- `{{ variable }}` to output a value.
- `{% for item in items %}...{% endfor %}` to loop.
- `{% if condition %}...{% endif %}` for conditional rendering.

---

### Step 1: Check Out the tut-8 Branch ✓
```bash
git checkout tut-8
```

### Step 2: Open the Key Files ✓
- Backend view: `app.py` (the `dashboard()` function passes data to the template)
- Frontend template: `templates/dashboard.html`

---

### Step 3: Complete the Backend Metrics (app.py) ✓
There is a TODO in `dashboard()` to calculate two metrics:

1) **Largest Expense** (`largest_expense`)
	 - Find the most negative transaction.
	 - Hint: `session.query(Transaction).filter(Transaction.amount < 0).order_by(Transaction.amount).first()`

2) **Average Transaction** (`avg_transaction`)
	 - Average all transaction amounts.
	 - Hint: `avg_transaction = sum(float(t.amount) for t in transactions) / len(transactions)` (guard for zero transactions).

Both variables are already passed to `render_template`; just compute them.

---

### Step 4: Build the New Metric Cards (templates/dashboard.html) ✓
Find the TODO comments in the metrics section. Add two cards using the same structure/classes as the existing cards:
This is **totally optional** and you will not be expected to know HTML / CSS for this course. The main point is to see how Jinja2 expressions work in a real template.

- **Largest Expense** card
	- Icon suggestion: 💸, 🔴, or ⚠️.
	- If `largest_expense` exists, show its description and amount with a leading minus sign.
	- Format example: `-{% raw %}{{{% endraw %} "%.2f"|format(largest_expense.amount|abs) {% raw %}}}{% endraw %}`
	- If none, show fallback text like “No expenses yet”.

- **Average Transaction** card
	- Icon suggestion: 📊 or 📈.
	- Display `avg_transaction` as currency: `R {% raw %}{{{% endraw %} "%.2f"|format(avg_transaction) {% raw %}}}{% endraw %}`.

Keep the classes: `metric-card`, `metric-card__icon`, `metric-card__label`, `metric-card__value` so styling stays consistent.

---

### Step 5: Run the App and Verify ✓
```bash
python app.py
```
Visit http://localhost:5000 and confirm:
- Both new cards appear.
- Largest Expense shows a negative amount and description (once you have expenses).
- Average Transaction shows a sensible value and updates when you add data.

---

### Step 6: (Optional) Add Data to See Changes
Use the “Add New Transaction” form on the dashboard to add an income and an expense, then refresh to see the cards update.

---

### Step 7: Run Tests
```bash
pytest tests/ -v
```
Ensure everything still passes.

---

### Step 8: Commit Your Work
1. Stage your changes (`app.py`, `templates/dashboard.html`).
2. Commit:
```bash
git commit -m "Completed Tutorial 8: Jinja2 dashboard metrics"
```

---

## Summary
- Templates let you mix static HTML with dynamic data supplied by Flask.
- Jinja2 provides `{{ ... }}` for values and `{% ... %}` for logic.
- You added two new dashboard cards by computing metrics in Flask and rendering them in the template.
- This mirrors real-world full-stack flow: database → Flask view → Jinja2 template → browser.

Great work—your dashboard now tells a richer financial story! 🎉