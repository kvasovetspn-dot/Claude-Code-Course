import { validators } from './validation.js';

const FIELDS = [
  { rowId: 'row-name',  inputId: 'name',  validate: validators.name },
  { rowId: 'row-phone', inputId: 'phone', validate: validators.phone },
  { rowId: 'row-email', inputId: 'email', validate: validators.email },
  { rowId: 'row-event', inputId: 'event', validate: validators.event },
];

export function submitForm(e) {
  e.preventDefault();
  let valid = true;

  FIELDS.forEach(({ rowId, inputId, validate }) => {
    const row = document.getElementById(rowId);
    const val = document.getElementById(inputId).value;
    const ok  = validate(val);
    row.classList.toggle('has-error', !ok);
    if (!ok) valid = false;
  });

  if (!document.getElementById('consent').checked) {
    valid = false;
    alert('Будь ласка, погодься на обробку персональних даних.');
  }

  if (!valid) return;

  const btn = e.target.querySelector('button[type=submit]');
  btn.textContent = '⏳ Надсилаємо…';
  btn.disabled = true;

  setTimeout(() => {
    document.getElementById('formView').style.display = 'none';
    document.getElementById('successView').classList.add('show');
    document.getElementById('regForm').reset();
    btn.textContent = '✦ Надіслати заявку';
    btn.disabled = false;
  }, 1200);
}
