document.querySelector(".btn").addEventListener("click", function () {
    document.querySelector(".format").classList.toggle("show");
});

document.addEventListener("DOMContentLoaded", () => {
    const messages = document.querySelectorAll(".message");

    messages.forEach(msg => {
        // Show animation (slide down)
        setTimeout(() => {
            msg.classList.add("show");
        }, 200); 

        // Hide animation after 3 seconds
        setTimeout(() => {
            msg.classList.remove("show");
        }, 3200);

        // Remove message from DOM after upward slide
        setTimeout(() => {
            msg.remove();
        }, 3800);
    });
});


