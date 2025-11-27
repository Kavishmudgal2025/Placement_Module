document.addEventListener("DOMContentLoaded", function () {
    const questionBlock = document.querySelector(".questions");

    // Check if any question label exists inside .questions
    const hasQuestions = questionBlock.querySelector(".question-block") !== null;

    // Show only if questions exist
    if (hasQuestions) {
        questionBlock.style.display = "block";
    } else {
        questionBlock.style.display = "none";
    }
});
