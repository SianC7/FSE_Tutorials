import os
from loguru import logger
from flask import Flask, jsonify, request

from customer_front.customer import customer_bp
from helpers.analysis import (
    display_transactions_by_category,
    generate_financial_charts,
    generate_text_report,
    get_category_names,
    get_transactions_by_category
)

app = Flask(__name__)
app.register_blueprint(customer_bp, url_prefix="/")


def main():
    logger.add("logs/app.log", rotation="1 MB")

    display_transactions_by_category("Job")
    display_transactions_by_category("Groceries")
    generate_financial_charts()
    logger.info("Financial Report:\n{}", generate_text_report())


# TODO Complete the API endpoint below
# NOTE You should use jsonify to return the report from generate_text_report()
@app.route("/api/financial_summary", methods=["GET"])
def api_financial_summary():
    """API endpoint to get the student-facing text report."""
    
    return jsonify(generate_text_report())


# TODO Complete the API endpoint below to return transactions for a specific category
# NOTE Accept a query parameter 'category' (e.g., /api/transactions?category=Groceries)
@app.route("/api/transactions", methods=["GET"])
def api_transactions_by_category():
    """API endpoint to get transactions filtered by category."""
    category = request.args.get("category")
    if not category:
        return jsonify({"error": "Category query parameter is required"}), 400
    
    transactions = get_transactions_by_category(category)
    return jsonify(transactions)


@app.route("/api/category", methods=["GET"])
def api_categories():
    """API endpoint to get a list of all categories."""
    return jsonify(get_category_names())


@app.route("/api/financial_charts", methods=["GET"])
def api_financial_charts():
    """Optionally generate charts and return web-friendly paths."""
    charts = generate_financial_charts()
    web_paths = {}
    for key, path in charts.items():
        if path:
            web_paths[key] = f"/static/{os.path.basename(path)}"
    return jsonify(web_paths)


if __name__ == "__main__":
    app.run(debug=True)
