const loginButton = document.querySelector("#login-link"),
    registerButton = document.querySelector("#register-link"),
    loginForm = document.querySelector("#login-form"),
    registerForm = document.querySelector("#register-form");


registerButton.onclick = function(e) {
    registerButton.classList.add('active');
    loginButton.classList.remove('active');

    loginForm.style.display = 'none';
    registerForm.style.display = 'block';
}

loginButton.onclick = function(e) {
    loginButton.classList.add('active')
    registerButton.classList.remove('active')

    loginForm.style.display = 'block';
    registerForm.style.display = 'none';
}
