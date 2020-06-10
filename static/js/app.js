(function(){
    var form = document.querySelector('#startstream');
    
    async function doStartStream(evt){
        evt.preventDefault();
        var url = 'server';
        var YOUTUBE_STREAM_KEY = document.querySelector('#YOUTUBE_STREAM_KEY').value;
        var TWITCH_STREAM_KEY = document.querySelector('#YOUTUBE_STREAM_KEY').value;
        var data = {
            'YOUTUBE_STREAM_KEY': YOUTUBE_STREAM_KEY,
            'TWITCH_STREAM_KEY': TWITCH_STREAM_KEY
        }
        var headers = {
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        }
        var resp = await fetch(url, {
            method:'POST', 
            body: JSON.stringify(data),
            headers: headers
        }); 
        const respJson = await resp.json();
        console.error('respJson', respJson);
        return false
    }
    function init(){
        form.addEventListener('submit', doStartStream);
    }
    init();
})();
