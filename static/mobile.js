document.addEventListener("DOMContentLoaded", function() {
    window.toggleRentalDays = function(id) {
        const rentalSection = document.getElementById(id);
        rentalSection.classList.toggle("hidden");
    };
});
