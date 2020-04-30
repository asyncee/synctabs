from injector import Binder
from injector import Injector

from synctabs.application.ports.password_service import PasswordService
from synctabs.application.ports.user_dao import UserDAO
from synctabs.infrastructure.password_service import BcryptPasswordService
from synctabs.infrastructure.user_dao import JsonUserDAO
from . import config
from .config import Config
from ..application.ports.tabs_dao import TabsDAO
from ..infrastructure.tabs_dao import JsonTabsDAO


def setup_di(binder: Binder) -> None:
    cfg = config.from_env()
    binder.bind(Config, to=cfg)
    binder.bind(PasswordService, BcryptPasswordService())  # type: ignore
    binder.bind(UserDAO, JsonUserDAO(cfg.USERS_FILE_PATH))  # type: ignore
    binder.bind(TabsDAO, JsonTabsDAO(cfg.TABS_FILE_PATH))  # type: ignore


def setup_injector() -> Injector:
    return Injector(setup_di)
