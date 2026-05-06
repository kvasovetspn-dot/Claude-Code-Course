import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { fireEvent } from '@testing-library/dom';
import { submitForm } from '@/form';

const FORM_HTML = `
  <div id="formView">
    <form id="regForm">
      <div class="form-row" id="row-name">
        <input id="name" type="text" />
        <span class="form-error"></span>
      </div>
      <div class="form-row" id="row-phone">
        <input id="phone" type="tel" />
        <span class="form-error"></span>
      </div>
      <div class="form-row" id="row-email">
        <input id="email" type="email" />
        <span class="form-error"></span>
      </div>
      <div class="form-row" id="row-event">
        <select id="event">
          <option value="">—</option>
          <option value="show">Show</option>
        </select>
        <span class="form-error"></span>
      </div>
      <input type="checkbox" id="consent" />
      <button type="submit">✦ Надіслати заявку</button>
    </form>
  </div>
  <div class="success-view" id="successView"></div>
`;

function attachAndFire() {
  const form = document.getElementById('regForm');
  form.addEventListener('submit', submitForm);
  fireEvent.submit(form);
}

function fillValidForm() {
  document.getElementById('name').value  = 'Марія Коваленко';
  document.getElementById('phone').value = '+380501234567';
  document.getElementById('email').value = 'maria@example.com';
  document.getElementById('event').value = 'show';
  document.getElementById('consent').checked = true;
}

describe('submitForm — validation errors', () => {
  beforeEach(() => {
    document.body.innerHTML = FORM_HTML;
    vi.spyOn(window, 'alert').mockImplementation(() => {});
  });

  afterEach(() => {
    document.body.innerHTML = '';
    vi.restoreAllMocks();
  });

  it('marks the name row as error when name is empty', () => {
    document.getElementById('phone').value = '+380501234567';
    document.getElementById('email').value = 'a@b.com';
    document.getElementById('event').value = 'show';
    document.getElementById('consent').checked = true;
    attachAndFire();
    expect(document.getElementById('row-name')).toHaveClass('has-error');
  });

  it('marks the phone row as error when phone is too short', () => {
    document.getElementById('name').value  = 'Марія';
    document.getElementById('email').value = 'a@b.com';
    document.getElementById('event').value = 'show';
    document.getElementById('consent').checked = true;
    attachAndFire();
    expect(document.getElementById('row-phone')).toHaveClass('has-error');
  });

  it('marks the email row as error for an invalid email', () => {
    document.getElementById('name').value  = 'Марія';
    document.getElementById('phone').value = '+380501234567';
    document.getElementById('email').value = 'not-an-email';
    document.getElementById('event').value = 'show';
    document.getElementById('consent').checked = true;
    attachAndFire();
    expect(document.getElementById('row-email')).toHaveClass('has-error');
  });

  it('marks the event row as error when no event is selected', () => {
    document.getElementById('name').value  = 'Марія';
    document.getElementById('phone').value = '+380501234567';
    document.getElementById('email').value = 'a@b.com';
    document.getElementById('consent').checked = true;
    attachAndFire();
    expect(document.getElementById('row-event')).toHaveClass('has-error');
  });

  it('shows multiple errors at once when several fields are invalid', () => {
    document.getElementById('consent').checked = true;
    attachAndFire();
    expect(document.getElementById('row-name')).toHaveClass('has-error');
    expect(document.getElementById('row-phone')).toHaveClass('has-error');
    expect(document.getElementById('row-email')).toHaveClass('has-error');
    expect(document.getElementById('row-event')).toHaveClass('has-error');
  });

  it('calls alert and blocks submission when consent is unchecked', () => {
    fillValidForm();
    document.getElementById('consent').checked = false;
    attachAndFire();
    expect(window.alert).toHaveBeenCalledOnce();
    expect(document.getElementById('successView')).not.toHaveClass('show');
  });

  it('clears an error class once the field becomes valid on resubmit', () => {
    attachAndFire(); // all fields empty — should mark errors
    expect(document.getElementById('row-name')).toHaveClass('has-error');

    fillValidForm();
    const form = document.getElementById('regForm');
    form.addEventListener('submit', submitForm);
    fireEvent.submit(form);
    expect(document.getElementById('row-name')).not.toHaveClass('has-error');
  });

  it('does not show the success view when validation fails', () => {
    attachAndFire();
    expect(document.getElementById('successView')).not.toHaveClass('show');
  });
});

describe('submitForm — successful submission', () => {
  beforeEach(() => {
    document.body.innerHTML = FORM_HTML;
    vi.useFakeTimers();
  });

  afterEach(() => {
    document.body.innerHTML = '';
    vi.useRealTimers();
    vi.restoreAllMocks();
  });

  it('disables the submit button immediately after submission', () => {
    fillValidForm();
    attachAndFire();
    expect(document.querySelector('button[type=submit]').disabled).toBe(true);
  });

  it('sets loading text on the submit button', () => {
    fillValidForm();
    attachAndFire();
    expect(document.querySelector('button[type=submit]').textContent).toContain('Надсилаємо');
  });

  it('shows the success view after the 1200 ms delay', () => {
    fillValidForm();
    attachAndFire();
    vi.advanceTimersByTime(1200);
    expect(document.getElementById('successView')).toHaveClass('show');
  });

  it('hides the form view after the 1200 ms delay', () => {
    fillValidForm();
    attachAndFire();
    vi.advanceTimersByTime(1200);
    expect(document.getElementById('formView').style.display).toBe('none');
  });

  it('re-enables and resets the submit button after the delay', () => {
    fillValidForm();
    attachAndFire();
    vi.advanceTimersByTime(1200);
    const btn = document.querySelector('button[type=submit]');
    expect(btn.disabled).toBe(false);
    expect(btn.textContent).toContain('Надіслати заявку');
  });

  it('resets the form fields after the delay', () => {
    fillValidForm();
    attachAndFire();
    vi.advanceTimersByTime(1200);
    expect(document.getElementById('name').value).toBe('');
    expect(document.getElementById('email').value).toBe('');
    expect(document.getElementById('phone').value).toBe('');
  });

  it('does not show success view before the delay elapses', () => {
    fillValidForm();
    attachAndFire();
    vi.advanceTimersByTime(800);
    expect(document.getElementById('successView')).not.toHaveClass('show');
  });
});
