import os
from dotenv import load_dotenv
from flask import Flask
from customer_front.customer import customer_bp
import logging
from loguru import logger

load_dotenv()


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


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def create_app(name=__name__):
    app = Flask(name)
    app.register_blueprint(customer_bp, url_prefix="/customer")
    app.secret_key = Config.get_secret_key()
    app.logger.handlers = []  # Clear default Flask logger handlers
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO, force=True)
    return app
