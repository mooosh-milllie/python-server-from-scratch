const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});

async function signUp(data) {
    const register = await fetch('http://localhost:5500/register', {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
          'Content-Type': 'application/json'
          // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    return register;
}
async function signIn(data) {
    const logIn = await fetch('http://localhost:5500/login', {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
          'Content-Type': 'application/json'
          // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    return logIn;
}
let signUpForm = document.getElementById('sign-up-form');

signUpForm.addEventListener('submit', async(event) => {
    event.preventDefault();
    const form = new FormData(event.target);
    const firstName = form.get("first-name");
    const lastName = form.get("last-name");
    const email = form.get("email");
    const password = form.get("password");
    var validRegex =  /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?/;
    const verifyPassword = form.get("verify-password");
    if (email.match(validRegex) && password === verifyPassword) {
        const data = {
            first_name: firstName,
            last_name: lastName,
            email: email,
            password: password,
            verify_password: verifyPassword
        }
        let registerResponse = await signUp(data);
        let body = await registerResponse.json();
        console.log(body);
        return
    }
    console.log('invalid registeration requirement')
})


// SIGN IN AS REGISTERED USER

let signInForm = document.getElementById('sign-in-form');

signInForm.addEventListener('submit', async(event) => {
    event.preventDefault();
    
    const form = new FormData(event.target);
    const email = form.get("email");
    const password = form.get("password");
    
    var validRegex =  /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?/;
    console.log(email.match(validRegex))
    if (password.length > 7 && email.match(validRegex)) {
        const data = {
            email: email,
            password: password,
        }
        let registerResponse = await signIn(data);
        let body = await registerResponse.json();
        console.log(body);
        if (body.data.message === 'LOGIN SUCESSFUL') {
            localStorage.setItem('authToken', JSON.stringify({token: body.data.token, firstName: body.data.name}))
            window.location.href = 'http://localhost:5500/home'
        }
    } else {
        console.log('invalid log in requirement')
    }
    
    
})