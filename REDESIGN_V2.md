# Redesign v2 — noticeable refresh (Pacific Dental Alliance)

This document describes a **second-phase visual redesign** beyond the earlier CSS polish. It is intentionally more distinctive: new typography, a cooler palette led by **teal** with **warm gold accents**, clearer hierarchy, and stronger section rhythm—while **keeping Bootstrap 4**, existing HTML structure, and all asset paths.

## Goals

- Read as a **modern healthcare / network** brand: calm, trustworthy, less “flat gold banner.”
- Improve **scanability** (navigation, heroes, cards, testimonials).
- Preserve **GitHub Pages** constraints (static files only, same `docs/` layout).
- Avoid editing **29+ HTML files** for structure; rely on **`main.css`** plus a **single shared font URL** change across pages.

## Typography

| Role | Before | After |
|------|--------|--------|
| Body & UI | Open Sans / Lato | **Plus Jakarta Sans** (400–700) |
| Display & headings | Lato | **Fraunces** (500–700, variable opsz via Google Fonts CSS2) |

Rationale: Jakarta reads crisp in UI and long copy; Fraunces adds **character** on heroes and section titles without feeling gimmicky. The existing wordmark SVG stays **near-black** (`#231F20`); it still works on a light bar.

## Color system

| Token (concept) | Direction |
|-----------------|-----------|
| Ink / text | Slate-based neutrals (`#334155`, `#64748b`) instead of olive-gray |
| Primary CTA | **Teal** (`#0f766e` → hover `#115e59`) — primary buttons, key accents |
| Gold accent | **Warm gold** (`#ca8a04` / `#d4a72c`) — headings highlights, coupons, link hover emphasis (evolution of legacy gold, not 1:1 `#BFBA3D`) |
| Surfaces | White, **cool gray bands** (`#f8fafc`, `#f1f5f9`), and a **mint-to-slate gradient** on the home feature band |
| Footer | **Deep navy gradient** (`#0c1929` → `#1e293b`) replacing flat near-black |
| Hero overlay | **Teal–navy diagonal gradient** over photography for stronger brand cast and legibility |

## Layout & components

- **Header:** Taller bar, **backdrop blur** + light border (where supported); **Appointments** CTA **visible from `lg` up** with reserved space so links don’t collide.
- **Hero:** Same images; new overlay; **Fraunces** headlines with tight tracking and light shadow.
- **Intro blocks:** Section titles **sentence case** (no forced all-caps); constrained line length for `.lead` retained.
- **Feature cards:** Taller radius, clearer hover (image dim, CTA shifts to **ink**), optional subtle **top highlight** on hover.
- **Testimonials:** Decorative giant quote **replaced** by a **left accent bar** + padding (cleaner, more editorial); portrait images use **large rounded corners** instead of perfect circles.
- **Locations accordion / practice extras:** Darker navy-teal headers, consistent card radius, unchanged behavior.
- **Coupons / offers:** Gold **left rail** + teal panel, aligned with new tokens.

## Accessibility

- **`:focus-visible`** rings use the new **teal** focus color.
- **Contrast:** Body text targets **slate-700** on white; gold is used mainly for **large headings** or accents, not small body text on cream.
- **`prefers-reduced-motion`:** Short transitions only; respect reduced motion (existing pattern kept).

## Files changed

| File | Change |
|------|--------|
| `docs/_assets/css/main.css` | Full restyle: `:root` tokens, typography, nav, hero, sections, cards, blockquote, footer, locations, details, coupons |
| All `docs/**/*.html` (same pattern as before) | Single Google Fonts `<link>` → Fraunces + Plus Jakarta Sans |

## Out of scope (future)

- Bootstrap 5 migration or component library swap.
- New photography or SVG logo recolor (would require asset work).
- Contact form backend (still static / external service).
- Rewriting copy or IA.

## Rollback

Revert `main.css` and the font `<link>` line in HTML to the previous **Lato + Open Sans** URL to return to the pre–v2 look.

---

*Version: 2.0 — documented and implemented together.*
