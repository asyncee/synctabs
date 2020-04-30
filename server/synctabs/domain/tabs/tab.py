from pydantic import BaseModel


class Tab(BaseModel):
    url: str
    title: str
    favIconUrl: str
