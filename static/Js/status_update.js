document.addEventListener("DOMContentLoaded", function () {
    // Get all round containers
    const round1 = document.querySelector(".round-system1");
    const round2 = document.querySelector(".round-system2");
    const round3 = document.querySelector(".round-system3");
    const round4 = document.querySelector(".round-system4");

    const rounds = [round1, round2, round3, round4];

    // Initially hide all except round 1
    for (let i = 1; i < rounds.length; i++) {
        rounds[i].style.display = "none";
    }

    function updateRounds() {
        for (let i = 0; i < rounds.length - 1; i++) {
            const checkbox = rounds[i].querySelector('input[type="checkbox"]');
            const nextRound = rounds[i + 1];
            if (checkbox.checked) {
                nextRound.style.display = "block";
            } else {
                // Hide next and all rounds after it
                for (let j = i + 1; j < rounds.length; j++) {
                    rounds[j].style.display = "none";
                    const cb = rounds[j].querySelector('input[type="checkbox"]');
                    cb.checked = false; // reset switch
                }
                break;
            }
        }
    }

    // Attach event listeners
    rounds.forEach((r) => {
        const checkbox = r.querySelector('input[type="checkbox"]');
        checkbox.addEventListener("change", updateRounds);
    });

    // Run once on load (in case some are pre-qualified)
    updateRounds();
});
