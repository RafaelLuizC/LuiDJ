document.addEventListener('readystatechange', function() {
    if (document.readyState !== "complete") {
        return;
    }

    const closeButtons = document.querySelectorAll('.btn-close');

    for (let closeButton of closeButtons) {
        closeButton.addEventListener('click', (event) => {
            event.currentTarget.closest('div').classList.remove('active');
        });
    }

    const navButtons = document.querySelectorAll('.nav-button');

    for (let navButton of navButtons) {
        navButton.addEventListener('click', (event) => {
            document.querySelector('.nav-button.active').classList.remove('active');
            event.currentTarget.classList.add('active');
            document.querySelector('.column.active').classList.remove('active');
            document.getElementById(event.currentTarget.dataset.toggle).classList.add('active');
        });
    }
});