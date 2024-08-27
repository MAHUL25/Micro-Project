document.addEventListener("DOMContentLoaded", function() {
    const tabs = document.querySelectorAll(".profile-sidebar ul li a");
    const profileTabs = document.querySelectorAll(".profile-tab");

    tabs.forEach(tab => {
        tab.addEventListener("click", function(event) {
            event.preventDefault();
            const target = document.querySelector(tab.getAttribute("href"));

            profileTabs.forEach(t => t.style.display = "none");
            target.style.display = "block";

            tabs.forEach(t => t.classList.remove("active"));
            tab.classList.add("active");
        });
    });

    // Show the first tab by default
    profileTabs[0].style.display = "block";
});
document.getElementById('logoutButton').addEventListener('click', function() {
    // Clear user session or remove token
    localStorage.removeItem('loggedInUser');
    // Redirect to login page
    window.location.href = 'login.html';
});

document.getElementById('showChangePasswordForm').addEventListener('click', function() {
    const formContainer = document.getElementById('changePasswordFormContainer');
    // Toggle the display of the form
    if (formContainer.style.display === "none") {
        formContainer.style.display = "block";
    } else {
        formContainer.style.display = "none";
    }
});
