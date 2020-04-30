from injector import inject
from pydantic import BaseModel

from synctabs.application.ports.password_service import PasswordService
from synctabs.application.ports.password_service import NotSecurePassword
from synctabs.application.ports.user_dao import UserDAO
from synctabs.domain.users.user import User


class AddUserInputDTO(BaseModel):
    username: str
    password: str


class AddUserUseCase:
    @inject
    def __init__(self, password_service: PasswordService, user_dao: UserDAO):
        self._password_service = password_service
        self._user_dao = user_dao

    def execute(self, request: AddUserInputDTO) -> None:
        secure_password = self._password_service.generate_password(
            NotSecurePassword(request.password)
        )
        user = User(username=request.username, password=secure_password)
        self._user_dao.save_user(user)
