import abc
from typing import List

from synctabs.domain.tabs.tab import Tab
from synctabs.domain.tabs.tabs_view import TabsView


class TabsDAO(abc.ABC):
    @abc.abstractmethod
    def get_view(self) -> TabsView:
        pass

    @abc.abstractmethod
    def write(self, tabs: List[Tab]) -> None:
        pass
