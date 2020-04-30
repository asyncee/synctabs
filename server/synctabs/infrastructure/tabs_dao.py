import datetime as dt
from typing import List
from typing import Optional

import orjson

from synctabs.application.ports.tabs_dao import TabsDAO
from synctabs.domain.tabs.tab import Tab
from synctabs.domain.tabs.tabs_view import TabsView


class JsonTabsDAO(TabsDAO):
    def __init__(self, filepath: str):
        self._filepath = filepath
        self._cache: Optional[TabsView] = None

    def get_view(self) -> TabsView:
        return self._cache or self._readfile()

    def write(self, tabs: List[Tab]) -> None:
        # Todo: lock file.
        view = TabsView(tabs=tabs, updated_at=dt.datetime.now(tz=dt.timezone.utc))
        with open(self._filepath, "wb") as f:
            self._cache = view
            content = orjson.dumps(view.dict())
            f.write(content)

    def _readfile(self) -> TabsView:
        try:
            with open(self._filepath, "r") as f:
                content = orjson.loads(f.read())
                return TabsView(**content)
        except FileNotFoundError:
            return TabsView(tabs=[], updated_at=dt.datetime.now(tz=dt.timezone.utc))
