import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { toggleMenu } from '@/menu';

describe('toggleMenu', () => {
  beforeEach(() => {
    document.body.innerHTML = '<ul id="navLinks"></ul>';
  });

  afterEach(() => {
    document.body.innerHTML = '';
  });

  it('adds "open" class when the menu is closed', () => {
    toggleMenu();
    expect(document.getElementById('navLinks')).toHaveClass('open');
  });

  it('removes "open" class when the menu is already open', () => {
    document.getElementById('navLinks').classList.add('open');
    toggleMenu();
    expect(document.getElementById('navLinks')).not.toHaveClass('open');
  });

  it('toggles back to open on a third call', () => {
    toggleMenu(); // open
    toggleMenu(); // close
    toggleMenu(); // open again
    expect(document.getElementById('navLinks')).toHaveClass('open');
  });
});
