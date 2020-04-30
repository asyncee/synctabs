import abc
from typing import NewType

from synctabs.domain.users.user import SecurePassword

NotSecurePassword = NewType("UnsecurePassword", str)


class PasswordService(abc.ABC):
    @abc.abstractmethod
    def generate_password(self, password: NotSecurePassword) -> SecurePassword:
        pass

    @abc.abstractmethod
    def check_password(self, plain: NotSecurePassword, secure: SecurePassword) -> bool:
        pass
