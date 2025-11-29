window.addEventListener('DOMContentLoaded', () => {
    const verifiedTick = document.createElement('div');
    verifiedTick.className = 'verified';
    verifiedTick.innerHTML = '&#10004; Verified';
    document.querySelector('.card').appendChild(verifiedTick);

    // Check if OTP verified flag exists in HTML (Django can render it)
    const isVerified = document.body.getAttribute('data-verified'); // add data-verified="true" in body if OTP verified
    if(isVerified === 'true'){
        verifiedTick.classList.add('show');
    }
});
