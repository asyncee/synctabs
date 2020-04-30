import datetime as dt
from typing import List

from pydantic import BaseModel

from synctabs.domain.tabs.tab import Tab


class TabsView(BaseModel):
    tabs: List[Tab]
    updated_at: dt.datetime
