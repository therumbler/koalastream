(function () {
    console.log('init');
    var form = document.querySelector('#signup');
    console.log(form);
    async function doSignup(evt) {
        evt.preventDefault();
        console.log('signup');
        const data = {
            password1: document.querySelector('#password1').value,
            password2: document.querySelector('#password2').value,
            email: document.querySelector('#email').value
        }
        const resp = await fetch('/users/signup', { method: 'POST', body: JSON.stringify(data) });
        console.log(await resp.json());
        return false;
    }
    form.addEventListener('submit', doSignup);

})();