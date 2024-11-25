// Function for the alert popup to create an attack

// Check if the attack_created flag is passed from the server
const attackCreated = {{ attack_created|tojson }};

// Display an alert if a new attack was successfully created
if (attackCreated) {
    alert("Attack created successfully!");
}

// Optional: Add additional alert or confirmation logic
// For example, confirmations before removing an attack or resetting fields
document.addEventListener("DOMContentLoaded", () => {
    const removeAttackButtons = document.querySelectorAll(".remove-attack-btn");

    // Confirmation dialog for removing an attack
    removeAttackButtons.forEach(button => {
        button.addEventListener("click", (event) => {
            const confirmRemove = confirm("Are you sure you want to remove this attack?");
            if (!confirmRemove) {
                // Prevent the form from being submitted
                event.preventDefault();
            }
        });
    });
});

