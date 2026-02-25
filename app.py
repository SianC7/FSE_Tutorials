from datetime import datetime
from transactions import Transaction, calculate_financial_summary
from decimal import Decimal

#TODO Investigate the error occurring in this main function, once fixed, uncomment the transaction on line 11.
def main():
    # Sample transactions, looks like we are saving nicely and have no expenses!
    transactions = [
        Transaction(description="Salary", amount=Decimal("5000"), category="income", date=datetime.now()),
        Transaction(description="Freelance Project", amount=Decimal("1500"), category="income", date=datetime.now()),
        Transaction(description="Gift", amount=Decimal("-2000"), category="expense", date=datetime.now()),
    ]
    # Uh oh! Something is going wrong... The line below this is causing an error. We should investigate.
    summary = calculate_financial_summary(transactions)
    print("Financial Summary:")
    for key, value in summary.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    









if __name__ == "__main__":
    main()
    


