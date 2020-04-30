import os
from pathlib import Path
from typing import Type

import dotenv


class Config:
    environment: str = ''

    USE_PRODUCTION_ASSETS: bool = True
    LOGIN_REQUIRED: bool = True
    USERS_FILE_PATH: str = ""
    TABS_FILE_PATH: str = ""
    ENABLE_API_DOCS: bool = False

    def __init__(self) -> None:
        self.USERS_FILE_PATH = str(Path(os.environ["USERS_FILE_PATH"]).expanduser())
        self.TABS_FILE_PATH = str(Path(os.environ["TABS_FILE_PATH"]).expanduser())


class DevelopmentConfig(Config):
    environment: str = "development"

    USE_PRODUCTION_ASSETS = False
    LOGIN_REQUIRED = False
    ENABLE_API_DOCS: bool = True


class ProductionConfig(Config):
    environment: str = "production"


def get_config(environment: str) -> Config:
    config: Type[Config]
    for config in [DevelopmentConfig, ProductionConfig]:
        if config.environment == environment:
            return config()

    raise RuntimeError(f"Unsupported environment: {environment}")


def from_env() -> Config:
    _load_environment()
    environment = os.getenv("ENVIRONMENT", "production")
    return get_config(environment)


def _load_environment() -> None:
    dotenv.load_dotenv(dotenv.find_dotenv())
