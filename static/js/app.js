(function () {
    var form = document.querySelector('#startstream');
    var token;
    async function call(endpoint, data, method) {
        if (method == undefined) {
            method = 'POST';
        }
        var headers = {
            'Authorization': 'Bearer ' + token
        }
        var resp = await fetch(url, {
            method: 'POST',
            body: JSON.stringify(data),
            headers: headers
        });
        const respJson = await resp.json();
        console.log('respJson', respJson);
        return respJson;
    }

    function logout() {
        window.localStorage.clear();
        init();
    }

    async function doStartStream(evt) {
        evt.preventDefault();
        var url = 'server';
        var YOUTUBE_STREAM_KEY = document.querySelector('#YOUTUBE_STREAM_KEY').value;
        var TWITCH_STREAM_KEY = document.querySelector('#TWITCH_STREAM_KEY').value;
        var TWITTER_STREAM_KEY = document.querySelector('#TWITTER_STREAM_KEY').value;
        var KS_STREAM_KEY = document.querySelector('#KS_STREAM_KEY').value;
        var data = {
            'YOUTUBE_STREAM_KEY': YOUTUBE_STREAM_KEY,
            'KS_STREAM_KEY': KS_STREAM_KEY,
            'TWITCH_STREAM_KEY': TWITCH_STREAM_KEY,
            'TWITTER_STREAM_KEY': TWITTER_STREAM_KEY
        }
        var headers = {
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        }
        var resp = await fetch(url, {
            method: 'POST',
            body: JSON.stringify(data),
            headers: headers
        });
        const respJson = await resp.json();
        console.error('respJson', respJson);
        return false
    }
    function init() {
        token = localStorage.getItem('token');
        if (!token) {
            var pathname = window.location.pathname;
            window.location.replace(pathname);
        }
        form.addEventListener('submit', doStartStream);
        document.querySelector('#logout').addEventListener("click", logout);
    }
    init();
})();
