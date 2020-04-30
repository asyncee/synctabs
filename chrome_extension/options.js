function save_options() {
    let host = document.getElementById('host').value;
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;
    chrome.storage.sync.set({
        host: host,
        username: username,
        password: password,
    }, function () {
        // Update status to let user know options were saved.
        let status = document.getElementById('status');
        status.textContent = 'Options saved.';
        setTimeout(function () {
            status.textContent = '';
        }, 750);
    });
}

function restore_options() {
    chrome.storage.sync.get({host: 'http://127.0.0.1:8000', username: ''}, function (items) {
        document.getElementById('host').value = items.host;
        document.getElementById('username').value = items.username;
        document.getElementById('password').value = '';
    });
}

document.addEventListener('DOMContentLoaded', restore_options);
document.getElementById('save').addEventListener('click',
    save_options);
