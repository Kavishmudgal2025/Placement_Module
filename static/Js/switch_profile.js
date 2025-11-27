// Optional JS: button click ripple effect

const buttons = document.querySelectorAll('.btn');

buttons.forEach(btn => {
    btn.addEventListener('click', function(e) {
        let ripple = document.createElement("span");
        ripple.classList.add("ripple");
        this.appendChild(ripple);

        setTimeout(() => ripple.remove(), 600);
    });
});
