from typing import NewType

from pydantic import BaseModel

SecurePassword = NewType("SecurePassword", str)


class User(BaseModel):
    username: str
    password: SecurePassword
