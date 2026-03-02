import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey") #os.getenv is used to get the value of an environment variable, if the variable is not set, it will return the default value provided as the second argument. In this case, if SECRET_KEY is not set in the environment, it will default to "supersecretkey".
    CURRENCY_SYMBOL = os.getenv("CURRENCY_SYMBOL", "R")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///finance.db")

    @classmethod
    def get_currency_symbol(cls: type) -> str:
        return cls.CURRENCY_SYMBOL

    @classmethod
    def get_secret_key(cls: type) -> str:
        return cls.SECRET_KEY

    @classmethod
    def get_database_url(cls: type) -> str:
        return cls.DATABASE_URL
