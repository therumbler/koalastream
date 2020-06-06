(function () {
    var formSignup = document.querySelector('#signup');
    var formLogin = document.querySelector('#login')

    var messages = document.querySelector('#messages');
    function handleError(respJson) {
        console.error(respJson);
        if (respJson.hasOwnProperty('error')) {
            console.error(respJson.error);
            messages.innerHTML = respJson.error;
        }
        if (respJson.hasOwnProperty('detail')) {
            console.error(respJson.detail);
            messages.innerHTML = respJson.detail[0].msg;
            var selector = '#' + respJson.detail[0].loc[respJson.detail[0].loc.length - 1];
            console.log('selector', selector);
            document.querySelector(selector).classList.add('error');
        }
    }
    function redirectToApp() {
        if (window.location.pathname.indexOf('/app') > -1) {
            return;
        }
        var pathname = window.location.pathname;
        var lastSlash = pathname.lastIndexOf('/');
        // if (lastSlash > 0) {
        pathname = pathname.substr(0, lastSlash) + '/app'

        // }
        console.log('pathname = ', pathname);
        window.location.replace(pathname)
    }
    function handleSuccess(form, respJson) {
        console.log('success');
        console.log(respJson);
        var reset = document.querySelector('input[type=reset]');
        reset.click();
        form.reset();
        messages.innerHTML = 'success';
        if (respJson.hasOwnProperty('token')) {
            localStorage.setItem('token', respJson.token);
            redirectToApp();
        }

    }
    async function doSignup(evt) {
        evt.preventDefault();
        messages.innerHTML = "";
        const data = {
            password1: document.querySelector('#password1').value,
            password2: document.querySelector('#password2').value,
            email: document.querySelector('#email').value
        }
        const resp = await fetch('./users/signup', { method: 'POST', body: JSON.stringify(data) });
        const respJson = await resp.json();
        if (resp.ok) {
            handleSuccess(evt.target, respJson);
        } else {
            handleError(respJson);
        }
        return false;
    }

    async function doLogin(evt) {
        evt.preventDefault();
        console.log(evt);
        messages.innerHTML = "";
        const data = {
            email: document.querySelector('#email').value,
            password: document.querySelector('#password').value
        }
        const resp = await fetch('./users/login', { method: 'POST', body: JSON.stringify(data) });
        const respJson = await resp.json();
        if (resp.ok) {
            handleSuccess(evt.target, respJson);
        } else {
            handleError(respJson);
        }
        return false;
    }
    if (formSignup) {
        formSignup.addEventListener('submit', doSignup);
    }
    if (formLogin) {
        formLogin.addEventListener('submit', doLogin);
    }

    function checkIsSignedIn() {
        var token = localStorage.getItem('token');
        if (token !== null) {
            console.log('already signed in');
            console.log(token);
            return true;
        }
        return false
    }
    function init() {
        var isSignedIn = checkIsSignedIn();
        if (!isSignedIn) {
            if (window.location.pathname.indexOf('app') > 0) {
                var pathname = window.location.pathname.replace('app', '');
                window.location.replace(pathname);
            }
        } else {
            redirectToApp();
        }
    }
    init();
})();
