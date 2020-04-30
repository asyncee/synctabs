from synctabs.application.add_user import AddUserInputDTO
from synctabs.application.add_user import AddUserUseCase
from synctabs.presentation.di import setup_injector


def add_user(username: str, password: str) -> None:
    injector = setup_injector()
    injector.get(AddUserUseCase).execute(
        AddUserInputDTO(username=username, password=password)
    )
