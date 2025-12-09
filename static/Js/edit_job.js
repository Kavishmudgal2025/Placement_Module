document.addEventListener("DOMContentLoaded", function() {
    const addButton = document.getElementById("add_button");
    const questionBlocks = document.querySelectorAll(".question-block");
    let currentVisible = 0;

    // Step 1: Show all questions that already have a valid (non-"N/A") value
    questionBlocks.forEach(block => {
        const input = block.querySelector("input[type='text']");
        if (input && input.value.trim() !== "" && input.value.trim().toUpperCase() !== "N/A") {
            block.style.display = "block";
            currentVisible++;
        } else {
            block.style.display = "none";
        }
    });

    // Step 2: Add click event for showing the next hidden (N/A or empty) question
    addButton.addEventListener("click", function() {
        // Find the next hidden question
        const nextHidden = Array.from(questionBlocks).find(block => block.style.display === "none");
        
        if (nextHidden) {
            nextHidden.style.display = "block";
            currentVisible++;

            // Smooth scroll to the newly shown question
            nextHidden.scrollIntoView({ behavior: "smooth", block: "center" });
        }

        // Disable the button if all are shown
        if (currentVisible === questionBlocks.length) {
            addButton.disabled = true;
            addButton.textContent = "All Questions Added";
        }
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const messages = document.querySelectorAll(".message");

    messages.forEach((msg) => {
        // show animation
        setTimeout(() => {
            msg.style.opacity = "1";
            msg.style.transform = "translateY(0)";
        }, 100);

        // hide after 3 seconds
        setTimeout(() => {
            msg.style.opacity = "0";
            msg.style.transform = "translateY(-20px)";
        }, 3000);

        // remove from DOM after animation (optional)
        setTimeout(() => {
            msg.remove();
        }, 3600);
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const messages = document.querySelectorAll(".message");

    messages.forEach(message => {
        // Show animation
        setTimeout(() => {
            message.style.opacity = "1";
            message.style.transform = "translateY(0)";
        }, 100); // slight delay so animation plays

        // Hide after 3 seconds
        setTimeout(() => {
            message.style.opacity = "0";
            message.style.transform = "translateY(-20px)";
        }, 3000);

        // Remove from DOM after animation
        setTimeout(() => {
            message.remove();
        }, 3600);
    });
});


