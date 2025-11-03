
console.log("JS Loaded");
// Add animation to form elements when they come into focus
document.querySelectorAll('.form-control').forEach(control => {
    control.addEventListener('focus', function() {
        this.parentElement.style.transform = 'scale(1.02)';
        this.parentElement.style.transition = 'transform 0.3s ease';
    });
    control.addEventListener('blur', function() {
        this.parentElement.style.transform = 'scale(1)';
    });
});
        
// Add date validation for deadline
const deadlineField = document.getElementById('deadline');
if(deadlineField) {
    const today = new Date().toISOString().split('T')[0];
    deadlineField.setAttribute('min', today);
}
        
// Prevent zoom on input focus for mobile
document.addEventListener('DOMContentLoaded', function() {
    let viewport = document.querySelector('meta[name="viewport"]');
    if (viewport) {
        function preventZoom(e) {
            if (e.touches.length > 1) {
                e.preventDefault();
                e.stopPropagation();
            }
        }
                
        document.addEventListener('touchstart', preventZoom, { passive: false });
        document.addEventListener('touchmove', preventZoom, { passive: false });
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const addButton = document.getElementById("add_button");
    const questionBlocks = document.querySelectorAll(".question-block");
    let currentVisible = 0;

    addButton.addEventListener("click", function () {
        if (currentVisible < questionBlocks.length) {
            questionBlocks[currentVisible].style.display = "block";
            currentVisible++;
        } else {
            alert("You can only add up to " + questionBlocks.length + " questions.");
        }
    });
});