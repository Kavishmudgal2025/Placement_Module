document.addEventListener("DOMContentLoaded", function () {

    // For each 3-state switch box
    document.querySelectorAll(".three-state-switch").forEach(box => {
        
        // All 3 radio buttons inside this switch
        const buttons = box.querySelectorAll(".button");

        // Smooth background animation
        box.style.transition = "background 0.5s ease";

        // Add change listener for each radio
        buttons.forEach(btn => {
            btn.addEventListener("change", () => {

                if (btn.value === "none") {
                    box.style.backgroundColor = "white";
                } 
                else if (btn.value === "disqualified") {
                    box.style.backgroundColor = "crimson";
                } 
                else if (btn.value === "qualified") {
                    box.style.backgroundColor = "rgba(30, 223, 88, 1)";
                }
            });
        });

        // Run once on page load to set correct color
        const checked = box.querySelector("input:checked");
        if (checked) {
            checked.dispatchEvent(new Event("change"));
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {

    const rounds = document.querySelectorAll(".round");

    // Hide all rounds except round 1
    for (let i = 1; i < rounds.length; i++) {
        rounds[i].style.display = "none";
    }

    // Add functionality for each three-state switch
    document.querySelectorAll(".three-state-switch").forEach(box => {

        const radios = box.querySelectorAll(".button");
        box.style.transition = "background 0.4s ease";

        radios.forEach(radio => {
            radio.addEventListener("change", () => {

                // Set the color of the switch
                if (radio.value === "none") {
                    box.style.backgroundColor = "white";
                } else if (radio.value === "disqualified") {
                    box.style.backgroundColor = "crimson";
                } else {
                    box.style.backgroundColor = "rgba(30, 223, 88, 1)";
                }

                updateRounds();
            });
        });

        // Apply stored selection on page load
        const checked = box.querySelector("input:checked");
        if (checked) checked.dispatchEvent(new Event("change"));
    });

    // Logic to display next round only if previous is qualified
    function updateRounds() {

        for (let i = 0; i < rounds.length - 1; i++) {

            const selected = rounds[i].querySelector(".three-state-switch input:checked");
            const nextRound = rounds[i + 1];

            if (!selected) continue;

            if (selected.value === "qualified") {
                nextRound.style.display = "block";
            } else {
                // Hide all subsequent rounds + reset them
                for (let j = i + 1; j < rounds.length; j++) {
                    rounds[j].style.display = "none";

                    // reset radios
                    const radios = rounds[j].querySelectorAll(".button");
                    radios.forEach(r => r.checked = false);

                    // reset background color
                    const box = rounds[j].querySelector(".three-state-switch");
                    if (box) box.style.backgroundColor = "white";
                }
                break;
            }
        }
    }

    // Handle initial visibility on page load
    updateRounds();
});
