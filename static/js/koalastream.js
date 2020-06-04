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
    function handleSuccess(respJson) {
        console.log('sucess');
    }
    async function doSignup(evt) {
        evt.preventDefault();
        const data = {
            password1: document.querySelector('#password1').value,
            password2: document.querySelector('#password2').value,
            email: document.querySelector('#email').value
        }
        const resp = await fetch('./users/signup', { method: 'POST', body: JSON.stringify(data) });
        const respJson = await resp.json();
        if (resp.ok) {
            handleSuccess(respJson);
        } else {
            handleError(respJson);
        }
        return false;
    }

    async function doLogin(evt) {
        evt.preventDefault();
        const data = {
            email: document.querySelector('#email').value,
            password: document.querySelector('#password').value
        }
        const resp = await fetch('./users/login', { method: 'POST', body: JSON.stringify(data) });
        const respJson = await resp.json();
        if (resp.ok) {
            handleSuccess(respJson)
        } else {
            handleError(respJson)
        }
        return false;
    }
    if (formSignup) {
        formSignup.addEventListener('submit', doSignup);
    }
    if (formLogin) {
        formLogin.addEventListener('submit', doLogin);
    }
})();
