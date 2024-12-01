// Function for the login popup

document.addEventListener("DOMContentLoaded", () => {
    const loginButton = document.querySelector(".auth-buttons .btn-outline-primary");
    const loginPopup = document.getElementById("loginPopup");
    const closePopup = document.getElementById("closePopup");

    // Show the popup when the login button is clicked
    loginButton.addEventListener("click", (e) => {
        e.preventDefault();                          // Prevent the default link behavior
        loginPopup.style.display = "block";          // Shows the popup
    });

    // Close the popup when the close button is clicked
    closePopup.addEventListener("click", () => {
        loginPopup.style.display = "none";                      // Hides the popup
    });

    // Close the popup when clicking outside of it
    window.addEventListener("click", (e) => {
        if (e.target === loginPopup) {
            loginPopup.style.display = "none";                 // Hides the popup
        }
    });
});
