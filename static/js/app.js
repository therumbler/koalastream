(function () {
    var form = document.querySelector('#startstream');
    var startStreamWrapper = document.querySelector('#start');
    var stopStreamWrapper = document.querySelector('#stop');
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
        console.log('respJson', respJson);
        localStorage.setItem('streamInfo', JSON.stringify(respJson));
        startStreamWrapper.style.display = 'none';
        stopStreamWrapper.style.display = '';
        displayRtmpUrl();
        return false
    }

    function displayRtmpUrl(){
        var streamInfo = JSON.parse(localStorage.getItem('streamInfo'));
        var rtmpUrl = window.location.host + ':' + streamInfo.port + '/' + streamInfo.ks_stream_key;
        document.querySelector('#messages').innerText = 'use ' + rtmpUrl + ' to stream';
    }
    async function doStopStream() {
        var streamInfo = localStorage.getItem('streamInfo')
        if(!streamInfo){
            console.error('no stream running');
            return;
        }
        streamInfo = JSON.parse(streamInfo);
        var containerId = streamInfo.container_id;
        url = 'server/'+ containerId;
        var headers = {
            'Authorization': 'Bearer ' + token
        }
        var resp = await fetch(url, {
            method: 'DELETE',
            headers: headers
        })
        if(resp.status >= 400){
            logger.error(url, 'returned error', resp.status)
            return
        }
        localStorage.removeItem('streamInfo')
        init();
    }
    function init() {
        token = localStorage.getItem('token');
        if (!token) {
            var pathname = window.location.pathname;
            window.location.replace(pathname);
        }
        form.addEventListener('submit', doStartStream);
        document.querySelector('#stop').addEventListener('click', doStopStream);
        document.querySelector('#logout').addEventListener("click", logout);
        streamInfo = localStorage.getItem('streamInfo')
        if (streamInfo){
            startStreamWrapper.style.display = 'none';
            stopStreamWrapper.style.display = '';
        }
    }
    init();
})();
