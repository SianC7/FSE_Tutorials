from loguru import logger

from transactions import Transaction, Category, calculate_financial_summary
from database import get_session
from sqlalchemy import select
from decimal import Decimal, InvalidOperation


def main():
    logger.add("logs/app.log", rotation="1 MB")
    # Initialize database and create tables
    # Get a session
    session = get_session()

    try:
        # Ensure transaction table exists by querying it
        session.query(Transaction).first()

        # Query all transactions from the database
        all_transactions = session.query(Transaction).all()

        # Calculate and display summary
        summary = calculate_financial_summary(all_transactions)
        print("Financial Summary:")
        for key, value in summary.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
    except Exception as e:
        logger.error(
            f"You may need to seed the database first, run 'python seed.py' and try again.\n\n"
        )
        raise e

    finally:
        session.close()
        # TODO: Once you have added the Entertainment category and sample  expenses, uncomment the lines below to display them!
        # display_transactions_by_category("Job")
        # display_transactions_by_category("Entertainment")


# TODO: Add the entertainment category, if it does not already exist ✓
# NOTE: This means checking if a category with that name exists first ✓
def add_entertainment_category():
    session = get_session() # Get a new session to interact with the database
    try:
        # Check if a category with the name "Entertainment" already exists in the database (just return the first instance of 
        # "Entertainment" that is found), var is set to True if it exists, False otherwise. 
        # is not None is used to convert the result of the query into a boolean value (True if a category is found, False if not)
        category_exists = session.query(Category).filter_by(name="Entertainment").first() is not None 
        if category_exists: # if the category already exists
            return # nothing to do, just return
        else:
            # If the category does not exist, create a new category with the name "Entertainment" and add it to the session.
            # Adding the category to the session marks it for insertion into the database when we commit the transaction.
            # Category(name="Entertainment") creates a new instance of the Category class with the name "Entertainment". 
            # This instance represents a new row in the categories table that we want to add to the database.
            session.add(Category(name="Entertainment")) 
            session.commit() # Commit the transaction to save the new category to the database
    finally:
        session.close() # Close the session with the database (frees up resources)


# TODO: Add sample entertainment expenses ✓
# NOTE: Fetch the Entertainment category first, then add two sample expenses (transaction instances) linked to that category ✓
def add_entertainment_expenses():
    session = get_session()
    try:
        # Step 1: Check if the Entertainment category exists.
        # Fetch the Entertainment category from the database (just return the first instance of "Entertainment" that is found)
        entertainment_category = session.query(Category).filter_by(name="Entertainment").first() # contains the category object if it exists, None otherwise
        
        # Step 2: If the category exists, fetch it from the database and create two sample expenses linked to that category.
        if entertainment_category: # if the category does exist
            
            # Create two sample expenses (transaction instances) linked to the Entertainment category.
            expense1 = Transaction(
                date="2024-06-01",
                description="Movie tickets",
                amount=Decimal("-50.00"), # Negative amount indicates an expense
                category_ref=entertainment_category, # Link the transaction to the Entertainment category using the category_ref relationship
            )
            expense2 = Transaction(
                date="2024-06-05",
                description="Concert tickets",
                amount=Decimal("-150.00"), # Negative amount indicates an expense
                category_ref=entertainment_category, # Link the transaction to the Entertainment category using the category_ref relationship
            )
            # Add the expenses to the session and commit the transaction to save them to the database.
            session.add_all([expense1, expense2]) # Add both expenses to the session at once
            # OR:
            # session.add(expense1)
            # session.add(expense2)
            
            # Step 3: Commit the transaction to save the new expenses to the database
            session.commit() # Commit the transaction to save the new expenses to the database
    finally:
        session.close()


# TODO: Display all transactions for a given category name
def display_transactions_by_category(category_name: str):
    session = get_session()
    try:
        # Step 1: Fetch the category by name
        category = session.query(Category).filter_by(name=category_name).first()
        if not category:
            print(f"No category found with name '{category_name}'")
            return
        
        # Step 2: Display transactions for the category
        print(f"Transactions for category '{category_name}':")
        
        # option 1: transations = session.query(Transaction).filter_by(category_id = category.id).all() # get all transactions that have a category_id that matches the id of the category we fetched, this will return a list of transaction objects that are linked to the category
        #           for transations in transations:
        #               print(transations)
        for transaction in category.transactions: # Access the transactions related to the category using the transactions relationship defined in the Category class
            print(transaction) # This will use the __repr__ method of the Transaction class to display the transaction details in a readable format
            
    except Exception as e:
        logger.error(
            f"Error displaying transactions for category '{category_name}': {e}"
        )
    finally:
        session.close()


if __name__ == "__main__":
    main()
