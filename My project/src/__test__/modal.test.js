import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { openModal, closeModal, closeOnBackdrop } from '@/modal';

const MODAL_HTML = `
  <div class="modal-overlay" id="modalOverlay">
    <div class="modal" id="modal">
      <div id="formView"></div>
      <div class="success-view" id="successView"></div>
      <p id="modalEventName"></p>
      <select id="event">
        <option value="">— Обери подію —</option>
        <option value="show">🎭 Вистава «Тіні забутих предків» — 24 травня</option>
        <option value="party">🎉 Етновечірка «Вечорниці 2026» — 31 травня</option>
        <option value="workshop">🧵 Майстер-клас з вишивки бісером — 7 червня</option>
        <option value="festival">🌸 Фестиваль «Своя Земля» — 21 червня</option>
      </select>
    </div>
  </div>
`;

describe('openModal', () => {
  beforeEach(() => {
    document.body.innerHTML = MODAL_HTML;
  });

  afterEach(() => {
    document.body.innerHTML = '';
    document.body.style.overflow = '';
  });

  it('makes the overlay visible by adding "open"', () => {
    openModal();
    expect(document.getElementById('modalOverlay')).toHaveClass('open');
  });

  it('locks body scroll', () => {
    openModal();
    expect(document.body.style.overflow).toBe('hidden');
  });

  it('resets formView display so it is visible', () => {
    document.getElementById('formView').style.display = 'none';
    openModal();
    expect(document.getElementById('formView').style.display).toBe('');
  });

  it('hides the success view if it was showing', () => {
    document.getElementById('successView').classList.add('show');
    openModal();
    expect(document.getElementById('successView')).not.toHaveClass('show');
  });

  it('shows default label text when called without an event name', () => {
    openModal();
    expect(document.getElementById('modalEventName').textContent).toContain('Заповни форму');
  });

  it('sets the label to the provided event name', () => {
    openModal('Вистава «Тіні забутих предків» — 24 травня');
    expect(document.getElementById('modalEventName').textContent)
      .toBe('Вистава «Тіні забутих предків» — 24 травня');
  });

  it('pre-selects the show option', () => {
    openModal('Вистава «Тіні забутих предків» — 24 травня');
    expect(document.getElementById('event').value).toBe('show');
  });

  it('pre-selects the party option', () => {
    openModal('Етновечірка «Вечорниці 2026» — 31 травня');
    expect(document.getElementById('event').value).toBe('party');
  });

  it('pre-selects the workshop option', () => {
    openModal('Майстер-клас з вишивки бісером — 7 червня');
    expect(document.getElementById('event').value).toBe('workshop');
  });

  it('pre-selects the festival option', () => {
    openModal('Фестиваль «Своя Земля» — 21 червня');
    expect(document.getElementById('event').value).toBe('festival');
  });

  it('leaves the dropdown on its default when no name matches', () => {
    openModal('Якась невідома подія — 1 січня');
    expect(document.getElementById('event').value).toBe('');
  });
});

describe('closeModal', () => {
  beforeEach(() => {
    document.body.innerHTML = MODAL_HTML;
    openModal();
  });

  afterEach(() => {
    document.body.innerHTML = '';
    document.body.style.overflow = '';
  });

  it('removes the "open" class from the overlay', () => {
    closeModal();
    expect(document.getElementById('modalOverlay')).not.toHaveClass('open');
  });

  it('restores body scroll', () => {
    closeModal();
    expect(document.body.style.overflow).toBe('');
  });
});

describe('closeOnBackdrop', () => {
  beforeEach(() => {
    document.body.innerHTML = MODAL_HTML;
    openModal();
  });

  afterEach(() => {
    document.body.innerHTML = '';
    document.body.style.overflow = '';
  });

  it('closes the modal when the backdrop overlay itself is the target', () => {
    const overlay = document.getElementById('modalOverlay');
    closeOnBackdrop({ target: overlay });
    expect(overlay).not.toHaveClass('open');
  });

  it('does not close the modal when an inner element is the target', () => {
    const inner = document.getElementById('modal');
    closeOnBackdrop({ target: inner });
    expect(document.getElementById('modalOverlay')).toHaveClass('open');
  });
});
