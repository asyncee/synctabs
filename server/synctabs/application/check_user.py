from injector import inject
from pydantic import BaseModel

from synctabs.application.ports.password_service import PasswordService
from synctabs.application.ports.password_service import NotSecurePassword
from synctabs.application.ports.user_dao import UserDAO
from synctabs.application.ports.user_dao import UserNotFound
from synctabs.domain.exception import DomainException


class AuthenticateUserInputDTO(BaseModel):
    username: str
    password: str


class AuthenticatedUser(BaseModel):
    username: str


class AuthenticationError(DomainException):
    pass


class InvalidUsername(AuthenticationError):
    pass


class InvalidPassword(AuthenticationError):
    pass


class AuthenticateUserUseCase:
    @inject
    def __init__(self, password_service: PasswordService, user_dao: UserDAO):
        self._password_service = password_service
        self._user_dao = user_dao

    def execute(self, request: AuthenticateUserInputDTO) -> AuthenticatedUser:
        try:
            user = self._user_dao.get_user(request.username)
        except UserNotFound:
            raise InvalidUsername

        if not self._password_service.check_password(
            NotSecurePassword(request.password), user.password
        ):
            raise InvalidPassword

        return AuthenticatedUser(username=request.username)
