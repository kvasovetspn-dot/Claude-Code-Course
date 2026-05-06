export const validators = {
  name:  v => v.trim().length > 1,
  phone: v => v.trim().length > 6,
  email: v => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v),
  event: v => v !== '',
};
