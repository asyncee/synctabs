import json
from json import JSONDecodeError

from synctabs.application.ports.user_dao import UserDAO
from synctabs.application.ports.user_dao import UserNotFound
from synctabs.domain.users.user import User


class JsonUserDAO(UserDAO):
    def __init__(self, filepath: str):
        self._filepath = filepath

    def get_user(self, username: str) -> User:
        user_not_found = UserNotFound(f"Can not find user with username '{username!r}'")

        try:
            with open(self._filepath, "r") as f:
                passwords = json.load(f)
                try:
                    return User(username=username, password=passwords[username])
                except KeyError:
                    raise user_not_found
        except FileNotFoundError:
            raise user_not_found

    def save_user(self, user: User) -> None:
        # todo: lock file
        with open(self._filepath, "w+") as f:
            try:
                passwords = json.load(f)
            except JSONDecodeError:
                passwords = {}

            passwords[user.username] = user.password
            f.write(json.dumps(passwords))
