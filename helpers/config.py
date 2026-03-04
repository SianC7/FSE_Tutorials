import os
from dotenv import load_dotenv

load_dotenv()


# TODO: Load SECRET_KEY and CURRENCY_SYMBOL from environment variables using python-dotenv
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    CURRENCY_SYMBOL = os.getenv("CURRENCY_SYMBOL", "R")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/finance.db")

    @classmethod
    def get_currency_symbol(cls: type) -> str:
        return cls.CURRENCY_SYMBOL

    @classmethod
    def get_secret_key(cls: type) -> str:
        return cls.SECRET_KEY

    @classmethod
    def get_database_url(cls: type) -> str:
        return cls.DATABASE_URL
