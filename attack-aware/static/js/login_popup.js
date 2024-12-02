// Function for the login popup

// LOGIN POPUP FUNCTIONALITY

const showPopupBtns = document.querySelectorAll('.btn-outline-primary');
const formPopup = document.querySelector('.login-popup');
const closePopupBtn = document.querySelector('.login-popup .close-btn');
const loginSignUpLink = document.querySelectorAll('.login-form .bottom-link a');

showPopupBtns.forEach(btn => {                        // Show Popup
    btn.addEventListener('click', () => {
        document.body.classList.add('show-popup');
    });
});

closePopupBtn.addEventListener('click', () => {       // Close Popup
    document.body.classList.remove('show-popup');
});

loginSignUpLink.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        formPopup.classList[link.id == "signup-link" ? 'add' : 'remove']('show-signup');
    });
});