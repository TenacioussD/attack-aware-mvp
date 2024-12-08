// LOGIN POPUP FUNCTIONALITY

const showPopupBtns = document.querySelectorAll('.btn-outline-primary');
const formPopup = document.querySelector('.login-popup');
const closePopupBtn = document.querySelector('.login-popup .close-btn');
const loginSignUpLink = document.querySelectorAll('.login-form .bottom-link a');
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');  // Extracts the CSRF token from the meta tag
const logoutBtn = document.getElementById('logout-btn'); // Gets the logout button


// Shows the popup when the user clicks on the login button
showPopupBtns.forEach(btn => {                        
    btn.addEventListener('click', () => {
        document.body.classList.add('show-popup');
    });
});

// Closes the popup when the user clicks on the close button
closePopupBtn.addEventListener('click', () => {  
    document.body.classList.remove('show-popup');
});

loginSignUpLink.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        formPopup.classList[link.id == "signup-link" ? 'add' : 'remove']('show-signup');
    });
});

// LOGOUT FUNCTIONALITY

logoutBtn.addEventListener('click', function(e) {
    e.preventDefault();                 // Prevents the default form submission

    // Hides the login popup before logout
    document.body.classList.remove('show-popup');
    
    // Creates a POST request using Fetch API
    fetch('/logout', {
        method: 'POST',       // POST request for logout
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded', 
            'X-CSRFToken': csrfToken    // Includes the CSRF token in the request header
        },
        body: new URLSearchParams({ csrf_token: csrfToken })  // Send CSRF token in the request body
    })

    .then(response => {
        if (response.ok) {
            window.location.href = '/';   // Redirects after logout
        } else {
            alert("Logout failed!");
        }
    })

    .catch(error => {
        console.error('Error during logout:', error);
    });
});