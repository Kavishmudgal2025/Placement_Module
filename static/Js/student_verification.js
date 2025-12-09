document.addEventListener("DOMContentLoaded", function () {
    let messages = document.querySelectorAll(".message");

    messages.forEach((msg) => {
        // Add slide-down class
        setTimeout(() => {
            msg.classList.add("show");
        }, 100);

        // Remove after 3 seconds
        setTimeout(() => {
            msg.classList.remove("show");
        }, 3000);
    });
});
