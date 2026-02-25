import os
from dotenv import load_dotenv

load_dotenv()


# TODO: Load SECRET_KEY and CURRENCY_SYMBOL from environment variables using python-dotenv
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "") # Get secret key from .enc file, default to empty string if not set
    CURRENCY_SYMBOL = os.getenv("CURRENCY_SYMBOL", "R") # Default to "R" if not set

    @classmethod
    def get_currency_symbol(cls : type) -> str:
        return cls.CURRENCY_SYMBOL
    
    @classmethod
    def get_secret_key(cls : type) -> str:
        return cls.SECRET_KEY