from pathlib import Path
from typing import Any

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPBasic
from fastapi.security import HTTPBasicCredentials
from starlette.templating import Jinja2Templates

from synctabs.application.check_user import AuthenticateUserInputDTO
from synctabs.application.check_user import AuthenticateUserUseCase
from synctabs.application.check_user import AuthenticatedUser
from synctabs.application.check_user import AuthenticationError
from synctabs.presentation.di import setup_injector

injector = setup_injector()

security = HTTPBasic()

templates = Jinja2Templates(
    directory=str(Path(__file__).parent.resolve() / "templates")
)


class On:
    def __init__(self, dependency: Any):
        self._dependency = dependency

    def __call__(self) -> Any:
        return injector.get(self._dependency)


def get_current_user(
    credentials: HTTPBasicCredentials = Depends(security),
    usecase: AuthenticateUserUseCase = Depends(On(AuthenticateUserUseCase)),
) -> AuthenticatedUser:
    try:
        return usecase.execute(
            AuthenticateUserInputDTO(
                username=credentials.username, password=credentials.password,
            )
        )
    except AuthenticationError:
        raise HTTPException(401, headers={"WWW-Authenticate": "Basic"})
