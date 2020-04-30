import bcrypt

from synctabs.application.ports.password_service import PasswordService
from synctabs.application.ports.password_service import NotSecurePassword
from synctabs.domain.users.user import SecurePassword


class BcryptPasswordService(PasswordService):
    def generate_password(self, password: NotSecurePassword) -> SecurePassword:
        salt = bcrypt.gensalt()
        return SecurePassword(
            bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
        )

    def check_password(self, plain: NotSecurePassword, secure: SecurePassword) -> bool:
        return bool(bcrypt.checkpw(plain.encode("utf-8"), secure.encode("utf-8")))
