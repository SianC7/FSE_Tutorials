from decimal import Decimal
import os
from loguru import logger
from flask import jsonify, redirect, render_template, request, url_for, flash

from helpers.analysis import (
    add_transaction_to_db,
    generate_financial_charts,
    generate_text_report,
    get_category_names,
    get_transactions_by_category,
    get_all_transactions,
    get_largest_expense,
    get_average_transaction_amount,
)
from helpers.config import Config, create_app

from tasks import generate_charts_task, log_transaction_audit_task
from helpers.analysis import add_category_to_db

# FLASK APP SETUP
app = create_app(__name__)

# FLASK APP


@app.route("/")
def dashboard():
    """Main dashboard with Jinja2 template."""
    # Get all transactions
    transactions = get_all_transactions()
    # Get financial report
    report = generate_text_report()
    # Generate charts and get paths
    chart_task = generate_charts_task.delay()  # type: ignore
    
    largest_expense = get_largest_expense()

    avg_transaction = get_average_transaction_amount()

    category_names = get_category_names()

    return render_template(
        "dashboard.html",
        transactions=transactions,
        report=report,
        chart_paths={},
        chart_task_id=chart_task.id,  # Pass the Celery task ID to the template
        largest_expense=largest_expense,
        avg_transaction=avg_transaction,
        category_names=category_names,
    )




#TODO You must call the audit transaction celery logging task here. Check dashboard and tasks.py for more details.
@app.route("/transaction/add", methods=["POST"])
def add_transaction():
    """Handle adding a new transaction."""
    transaction_id = None
    try:
        # Extract form data
        date_str = request.form.get("date")
        description = request.form.get("description")
        amount = Decimal(request.form.get("amount", "0"))
        category = request.form.get("category")

        transaction_id  = add_transaction_to_db(
            date=date_str,
            description=description,
            amount=amount,
            category_name=category,
        )
        flash("Transaction added successfully!", "success")
    except Exception as e:
        logger.error(f"Error adding transaction: {e}")
        flash(f"Error adding transaction: {str(e)}", "error")
    if transaction_id is not None:
      log_transaction_audit_task.delay(transaction_id)  # type: ignore
      pass

    

    return redirect(url_for("dashboard"))


@app.route("/category/add", methods=["POST"])
def add_category():
    """Handle adding a new category."""
    try:
        category_name = request.form.get("category_name", "").strip()

        if not category_name:
            flash("Category name cannot be empty", "error")
        else:
            add_category_to_db(category_name)
            flash(f'Category "{category_name}" added successfully!', "success")
    except Exception as e:
        logger.error(f"Error adding category: {e}")
        flash(f"Error adding category: {str(e)}", "error")

    return redirect(url_for("dashboard"))


# API ENDPOINTS


@app.route("/api/financial_summary", methods=["GET"])
def api_financial_summary():
    """API endpoint to get the student-facing text report."""
    return jsonify(generate_text_report())


@app.route("/api/transactions", methods=["GET"])
def api_transactions_by_category():
    """API endpoint to get transactions filtered by category."""
    category = request.args.get("category")
    if not category:
        return jsonify({"error": "Category query parameter is required"}), 400
    return jsonify(get_transactions_by_category(category))


@app.route("/api/category", methods=["GET"])
def api_categories():
    """API endpoint to get a list of all categories."""
    return jsonify(get_category_names())


@app.route("/api/financial_charts", methods=["GET"])
def api_financial_charts():
    """Generate charts synchronously."""
    charts = generate_financial_charts()
    web_paths = {}
    for key, path in charts.items():
        if path:
            web_paths[key] = f"/static/{os.path.basename(path)}"
    return jsonify(web_paths)


@app.route("/api/chart-status/<task_id>", methods=["GET"])
def chart_status(task_id):
    """Poll the status of chart generation task and return paths when ready."""
    task = generate_charts_task.AsyncResult(task_id)  # type: ignore

    if task.state == "PENDING":
        return jsonify(
            {"state": "pending", "status": "Chart generation in progress..."}
        )
    elif task.state == "SUCCESS":
        return jsonify({"state": "success", "chart_paths": task.result})
    elif task.state == "FAILURE":
        return jsonify({"state": "failure", "error": str(task.info)}), 500
    else:
        return jsonify({"state": task.state})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=Config.get_debug_mode())
