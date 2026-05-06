export function openModal(eventName) {
  const overlay = document.getElementById('modalOverlay');
  const select  = document.getElementById('event');
  const label   = document.getElementById('modalEventName');

  if (eventName) {
    label.textContent = eventName;
    const opts = select.options;
    for (let i = 0; i < opts.length; i++) {
      if (opts[i].text.includes(eventName.split('—')[0].trim().replace(/^[🎭🎉🧵🌸]\s*/, ''))) {
        select.selectedIndex = i;
        break;
      }
    }
  } else {
    label.textContent = 'Заповни форму — і ми надішлемо підтвердження на твою пошту.';
  }

  document.getElementById('formView').style.display = '';
  document.getElementById('successView').classList.remove('show');
  overlay.classList.add('open');
  document.body.style.overflow = 'hidden';
}

export function closeModal() {
  document.getElementById('modalOverlay').classList.remove('open');
  document.body.style.overflow = '';
}

export function closeOnBackdrop(e) {
  if (e.target === document.getElementById('modalOverlay')) closeModal();
}
