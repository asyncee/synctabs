var bus = new Vue();

var app = new Vue({
    el: '#app',
    data: {
        view: window.view
    },
    created(){
        bus.$on('set-view', (data)=> {
             this.view = data.view
        })
    }
})

function wsConnect(ws_scheme) {
    var ws = new WebSocket(ws_scheme + "://" + window.location.host + "/ws");
    ws.onmessage = function (e) {
        var request = JSON.parse(e.data)
        if (request.id === "new_view") {
            bus.$emit('set-view', {"view": request.view})
        }
    };

    ws.onclose = function (e) {
        setTimeout(function () {
            wsConnect();
        }, 1000);
    };

    ws.onerror = function (e) {
        console.error('Websocket error: ', e.message);
        ws.close();
    };
}

wsConnect(window.websocketScheme);
