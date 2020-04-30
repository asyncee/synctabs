async function post(url = '', data = {}, credentials = undefined) {
    let headers = new Headers({
        'Content-Type': 'application/json'
    })

    if (credentials) {
        headers.set('Authorization', 'Basic ' + btoa(
            credentials.username + ":" + credentials.password))
    }

    await fetch(url, {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        headers: headers,
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(data)
    });
}

function getSyncUrl() {
    return new Promise((resolve, reject) =>
        chrome.storage.sync.get(['host'], function (items) {
            resolve(items.host + '/sync');
        }))
}

function getCredentials() {
    return new Promise((resolve, reject) =>
        chrome.storage.sync.get(['username', 'password'], function (items) {
            resolve({username: items.username, password: items.password})
        }))
}

function getTabs() {
    return new Promise((resolve, reject) =>
        chrome.tabs.query({}, function (tabs) {
            resolve(tabs)
        }))
}

function synchronizeTabs() {
    Promise.all([getSyncUrl(), getCredentials(), getTabs()]).then(values => {
        let [url, credentials, tabs] = values;
        let postData = [];
        for (let tab of tabs) {
            postData.push({
                "url": tab.url,
                "title": tab.title,
                "favIconUrl": tab.favIconUrl || ""
            })
        }
        post(url, postData, credentials)
    })
}

function debouncedSynchronizeTabs() {
    chrome.alarms.clear("synchronize")
    chrome.alarms.create("synchronize", {when: Date.now() + 500})
}

chrome.alarms.onAlarm.addListener(function (alarm) {
    if (alarm.name !== "synchronize") return;

    synchronizeTabs()

    chrome.alarms.clear("synchronize")
})

chrome.tabs.onCreated.addListener(function (tab) {
    debouncedSynchronizeTabs()
})
chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
    debouncedSynchronizeTabs()
})
chrome.tabs.onMoved.addListener(function (tabId, moveInfo) {
    debouncedSynchronizeTabs()
})
chrome.tabs.onRemoved.addListener(function (tabId, removeInfo) {
    debouncedSynchronizeTabs()
})
chrome.tabs.onReplaced.addListener(function (addedTabId, removedTabId) {
    debouncedSynchronizeTabs()
})
chrome.browserAction.onClicked.addListener(function (ev) {
    debouncedSynchronizeTabs()
});
