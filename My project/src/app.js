import { toggleMenu }                          from './menu.js';
import { openModal, closeModal, closeOnBackdrop } from './modal.js';
import { submitForm }                            from './form.js';

window.toggleMenu      = toggleMenu;
window.openModal       = openModal;
window.closeModal      = closeModal;
window.closeOnBackdrop = closeOnBackdrop;
window.submitForm      = submitForm;

document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

const observer = new IntersectionObserver(
  entries => entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); }),
  { threshold: 0.12 }
);
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
