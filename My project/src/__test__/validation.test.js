import { describe, it, expect } from 'vitest';
import { validators } from '@/validation';

describe('validators.name', () => {
  it('accepts a valid full name', () => {
    expect(validators.name('Марія Коваленко')).toBe(true);
  });

  it('rejects empty string', () => {
    expect(validators.name('')).toBe(false);
  });

  it('rejects a single character', () => {
    expect(validators.name('М')).toBe(false);
  });

  it('rejects whitespace-only string', () => {
    expect(validators.name('   ')).toBe(false);
  });

  it('accepts a two-character name', () => {
    expect(validators.name('AB')).toBe(true);
  });

  it('trims before checking length', () => {
    expect(validators.name(' A ')).toBe(false);
  });
});

describe('validators.phone', () => {
  it('accepts a valid phone number', () => {
    expect(validators.phone('+380501234567')).toBe(true);
  });

  it('accepts a formatted phone number', () => {
    expect(validators.phone('+38 (050) 123 45 67')).toBe(true);
  });

  it('rejects empty string', () => {
    expect(validators.phone('')).toBe(false);
  });

  it('rejects a 6-character string (not > 6)', () => {
    expect(validators.phone('123456')).toBe(false);
  });

  it('accepts a 7-character string', () => {
    expect(validators.phone('1234567')).toBe(true);
  });

  it('rejects whitespace-padded short value', () => {
    expect(validators.phone('  123  ')).toBe(false);
  });
});

describe('validators.email', () => {
  it('accepts a standard email address', () => {
    expect(validators.email('user@example.com')).toBe(true);
  });

  it('accepts a subdomain email', () => {
    expect(validators.email('user@mail.example.com')).toBe(true);
  });

  it('rejects an address without @', () => {
    expect(validators.email('userexample.com')).toBe(false);
  });

  it('rejects an address without a domain', () => {
    expect(validators.email('user@')).toBe(false);
  });

  it('rejects an address without a TLD', () => {
    expect(validators.email('user@example')).toBe(false);
  });

  it('rejects an address with a space', () => {
    expect(validators.email('us er@example.com')).toBe(false);
  });

  it('rejects empty string', () => {
    expect(validators.email('')).toBe(false);
  });
});

describe('validators.event', () => {
  it('accepts a non-empty event value', () => {
    expect(validators.event('show')).toBe(true);
    expect(validators.event('party')).toBe(true);
    expect(validators.event('workshop')).toBe(true);
    expect(validators.event('festival')).toBe(true);
  });

  it('rejects empty string (the placeholder option value)', () => {
    expect(validators.event('')).toBe(false);
  });
});
