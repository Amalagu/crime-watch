const menuBtn = document.querySelector('#menu-btn')
const navLinks = document.querySelector('#nav-links')
menuBtn.addEventListener('click', () => {
    if(window.innerWidth < 1024) {
        navLinks.classList.toggle('nav--open')
        return
    } else {
        navLinks.classList.remove('nav--open')
        return
    }
})