from loguru import logger
from data.database import init_db

from helpers.analysis import (
    display_transactions_by_category,
    generate_financial_charts,
    generate_text_report,
)


def main():
    logger.add("logs/app.log", rotation="1 MB")
    init_db()

    display_transactions_by_category("Job")
    display_transactions_by_category("Groceries")
    generate_financial_charts()
    logger.info("Financial Report:\n{}", generate_text_report())


# This function should group and display transactions by category, so we can see like Income - 3 transactions, Expense - 2 transactions, etc.


if __name__ == "__main__":
    main()
