// dashboard.js

// Add a confirmation dialog before logging out
const logoutButton = document.getElementById("logoutButton");

logoutButton.addEventListener("click", function (e) {
    e.preventDefault(); // Prevent the default action
    
    const confirmed = window.confirm("Are you sure you want to log out?");
    
    if (confirmed) {
        // User confirmed, perform the logout action
        window.location.href = "{{ url_for('logout') }}"; // Replace with your actual logout URL
    }
});