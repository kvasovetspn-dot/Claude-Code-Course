# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Projects in this repository

This repo contains two independent projects:

1. **`My project/`** — СвоєРідне landing page (vanilla JS + Vitest)
2. **`OOP exam/`** — Python OOP exam exercises

---

## My project — СвоєРідне Landing Page

### Commands

All commands must be run from inside `My project/`:

```bash
cd "My project"
npm test          # run tests once (vitest run)
npm run test:watch  # watch mode
```

No build step — open `My project/index.html` directly in a browser (ESM, no bundler).

### Architecture

The page is a single HTML file (`index.html`) with all CSS inlined in `<style>`. All JS is loaded as an ES module from `src/app.js`.

**Module layout (`src/`):**
- `app.js` — entry point; imports the four feature modules and attaches them to `window` for use in inline HTML event handlers; also wires up the scroll-reveal `IntersectionObserver` and Escape key listener.
- `menu.js` — `toggleMenu()`: hamburger nav open/close.
- `modal.js` — `openModal(eventName?)`, `closeModal()`, `closeOnBackdrop(e)`: registration modal lifecycle. `openModal` optionally pre-selects the event in the `<select>` by matching the button's event name string.
- `form.js` — `submitForm(e)`: validates the four required fields using `validators`, shows inline errors, simulates a 1200 ms async submission, then swaps `#formView` for `#successView`.
- `validation.js` — `validators` object: pure functions for `name`, `phone`, `email`, and `event` fields.

**Testing (`src/__test__/`):**
- Uses Vitest + jsdom + `@testing-library/jest-dom`.
- Setup file (`setup.js`) extends Vitest's `expect` with jest-dom matchers.
- Tests reconstruct minimal DOM HTML in `beforeEach` and tear it down in `afterEach` — no shared state between tests.
- Path alias `@` maps to `src/` (configured in `vitest.config.js`).

### Key constraints
- No bundler — imports must use explicit `.js` extensions.
- Global functions (`openModal`, `closeModal`, etc.) are exposed via `window` because HTML uses inline `onclick` attributes.

---

## OOP exam — Python exercises

Run directly with Python (no dependencies):

```bash
python "OOP exam/oop_tasks.py"   # runs the demo
python -m pytest "OOP exam/"     # runs the test suite (pytest required)
```

Five tasks covering: abstract shape hierarchy, bank account encapsulation/inheritance, animal polymorphism, library composition with magic methods, and a generic Stack with iteration protocol.

---

## Business Context: СвоєРідне

This project belongs to a Ukrainian cultural events startup called **СвоєРідне**, founded by Anastasiia Kvasovetss. It brings Ukrainian ethnic culture to life through interactive, modern formats — ethno-parties, festivals, shows, and workshops — as an alternative to outdated museum-style institutions.

### Ціннісна пропозиція.pdf — Value Proposition Canvas

Describes the value map and client profile:

- **Client pains:** loneliness, monotony of cultural programs, alienation from Ukrainian culture due to its non-interactive presentation.
- **Client needs:** meaningful leisure, community belonging, discovering Ukrainian culture in a new way, attending workshops, singing/dancing, meeting new people.
- **Value delivered:** ethno-events in new formats (shows, parties, festivals, workshops), interactive elements (karaoke, dance floors, auctions, crafts, competitions), expert guest invitations (singers, craftspeople, dancers, photographers), casual meetups "for tea or coffee", monthly symbolic branded gifts (ethnic-style bracelets).
- **Core statement:** СвоєРідне provides authentic cultural experiences in interactive form, unlike museums and state institutions that use outdated formats.

### Бізнес-модель.pdf — Business Model Canvas

Covers the full business model:

- **Key partners:** cultural centers (Народний дім "Просвіта"), universities (УКУ, СО УКУ), donors and social funds (УКФ, USAID, Goethe-Institut), local cultural workers, school-friend founding team.
- **Key activities:** partner engagement, marketing and finance, Ukrainian heritage research, blogging and SMM, organizing events and workshops.
- **Customer segments:** culture-lovers, students and youth (18–35), parents engaging children in Ukrainian culture, companies ordering corporate ethno-events.
- **Revenue streams:** ticket sales; future — corporate events, consulting state institutions, fundraising.
- **Channels:** Instagram/Facebook, partner networks (cultural centers, museums, universities).

## Code Style

- Use comments sparingly. Only comment complex or non-obvious code.
