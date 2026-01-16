 const msg = document.querySelector('.messages');

  if (msg) {
    // trigger slide in
    setTimeout(() => msg.classList.add('show'), 50);

    setTimeout(() => msg.classList.remove('show'), 4000);
  }