


document.addEventListener('DOMContentLoaded', function() {
    const userAuthLink = document.getElementById('user-auth-link');
    const userName = sessionStorage.getItem('userName');

    if (userName) {
        userAuthLink.innerHTML = `<a href="profile.html"><i class="fas fa-user"></i>${userName}</a>`;
    } else {
        userAuthLink.innerHTML = `<a href="login.html">Login</a>`;
    }
});

// Function to handle login
function handleLogin(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Mockup: Replace this with actual authentication logic
    if (username === "testuser" && password === "password123") {
        sessionStorage.setItem('userName', username);
        window.location.href = "profile.html";
    } else {
        alert('Invalid credentials, please try again.');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const profileUsername = document.getElementById('profile-username');
    const userName = sessionStorage.getItem('userName');

    if (profileUsername && userName) {
        profileUsername.textContent = userName;
    }

    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) {
        logoutButton.addEventListener('click', function() {
            sessionStorage.removeItem('userName');
            window.location.href = "login.html";
        });
    }
});


// Handle user sign-up
function handleSignup(event) {
    event.preventDefault();
    const username = document.getElementById('signup-username').value;
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;

    // Mockup: Save user data in localStorage (for demonstration purposes)
    const user = {
        username: username,
        email: email,
        password: password
    };

    // Check if the user already exists
    if (localStorage.getItem(username)) {
        alert('Username already exists. Please choose a different one.');
    } else {
        localStorage.setItem(username, JSON.stringify(user));
        alert('Sign up successful! You can now log in.');
        window.location.href = "login.html";
    }
}

// Handle user login
function handleLogin(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const storedUser = JSON.parse(localStorage.getItem(username));

    if (storedUser && storedUser.password === password) {
        sessionStorage.setItem('userName', storedUser.username);
        window.location.href = "profile.html";
    } else {
        alert('Invalid credentials, please try again.');
    }
}


// Function to add item to cart
function addToCart(name, price, image) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    cart.push({name, price, image});
    localStorage.setItem('cart', JSON.stringify(cart));
}

// Event listener for add to cart buttons
document.querySelectorAll('.add-to-cart').forEach(button => {
    button.addEventListener('click', function() {
        const name = this.getAttribute('data-name');
        const price = this.getAttribute('data-price');
        const image = this.getAttribute('data-image');
        addToCart(name, price, image);
        alert(`${name} has been added to your cart!`);
    });
});

