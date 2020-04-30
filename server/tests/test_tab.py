from synctabs.domain.tabs.tab import Tab


def test_tab_entity():
    tab = Tab(url="url", title="title", favIconUrl="favicon")
    assert tab.url == "url"
    assert tab.title == "title"
    assert tab.favIconUrl == "favicon"
