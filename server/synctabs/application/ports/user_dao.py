import abc

from synctabs.domain.exception import DomainException
from synctabs.domain.users.user import User


class UserNotFound(DomainException):
    pass


class UserDAO(abc.ABC):
    @abc.abstractmethod
    def get_user(self, username: str) -> User:
        pass

    @abc.abstractmethod
    def save_user(self, user: User) -> None:
        pass
