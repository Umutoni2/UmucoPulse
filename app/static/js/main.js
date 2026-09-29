document.addEventListener('DOMContentLoaded', function () {
  const menuToggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.main-nav');
  const backToTopBtn = document.querySelector('.back-to-top');

  if (menuToggle && nav) {
    menuToggle.addEventListener('click', function () {
      const isActive = nav.classList.toggle('active');
      menuToggle.setAttribute('aria-expanded', isActive ? 'true' : 'false');
    });
  }

  if (backToTopBtn) {
    backToTopBtn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    window.addEventListener('scroll', function () {
      if (window.scrollY > 400) {
        backToTopBtn.classList.add('visible');
      } else {
        backToTopBtn.classList.remove('visible');
      }
    });
  }

  const flashMessages = document.querySelectorAll('.flash');
  flashMessages.forEach(function (flash) {
    setTimeout(function () {
      flash.classList.add('fade-out');
      setTimeout(function () { flash.remove(); }, 400);
    }, 5000);
  });
});
