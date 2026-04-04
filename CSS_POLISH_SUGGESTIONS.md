# CSS-only polish — suggestions

**Superseded for look & feel:** A more noticeable **redesign v2** is documented in **[REDESIGN_V2.md](REDESIGN_V2.md)** (Fraunces + Plus Jakarta Sans, teal-led palette, stronger section styling). The checklist below still helps if you want to tweak individual tokens.

Earlier polish (Lato / Open Sans era) has been replaced by v2 in `main.css`.

The stack stays **Bootstrap 4.0** + **Open Sans** / **Lato**; polish is mostly tokens, spacing, radius, shadows, and accessibility.

---

## 1. Add design tokens at the top of `main.css`

The file already hints at variables in a comment but uses raw hex everywhere. A `:root` block makes tuning fast and keeps the brand recognizable.

Suggested tokens (map to your existing palette):

| Token idea | Current equivalents in file |
|------------|-------------------------------|
| `--color-text` | `#606051` on `body` |
| `--color-text-muted` | `#44443a` (features, overview) |
| `--color-bg` | `#ffffff` |
| `--color-surface-warm` | `#F0ECDF` (`.bg-light`, sections) |
| `--color-surface-cool` | `#e0e7e7`, `#d1dcdc`, teals |
| `--color-primary` | `#BFBA3D` (gold accent) |
| `--color-primary-hover` | `#5A581D` |
| `--color-dark` | `#0D0D0B` |
| `--color-teal` / `--color-teal-dark` | `#577171`, `#405555`, `#89A5A5`, etc. |
| `--radius-sm` / `--radius-md` | new (see below) |
| `--shadow-nav` | from `#navMain` box-shadow |
| `--space-section` | vertical rhythm for `.intro`, `#HmSecFeatures`, etc. |

**Why:** One place to darken text slightly for contrast or soften backgrounds without hunting through 300+ lines.

---

## 2. Typography (CSS-only where possible)

| Area | Current | Suggestion |
|------|---------|------------|
| `h1` | `3.5rem` fixed | Use `clamp(2rem, 5vw, 3.25rem)` for smoother scaling; keep `line-height` ~1.1–1.2. |
| `h2` uppercase | Strong gold everywhere | Keep gold for section labels; consider **slightly** reducing `letter-spacing` (e.g. `0.03em`) so it feels less “2005 brochure.” |
| `body` | Open Sans | Optional later: add **`font-weight: 400` and `500`** in the Google Fonts URL in HTML for clearer hierarchy without changing font family. |
| `.lead` | `line-height: 1.7` | Bump to **1.65–1.75** and ensure `max-width: 38rem` on `.intro .lead` (centered block) so line length stays readable. |

**HTML note (optional, not CSS-only):** Loading `Lato:400,700` and `Open+Sans:400,600` improves hierarchy without switching families.

---

## 3. Buttons (`.btn`, `.btn-primary`, `.btn-secondary`, `.btn-xs`)

| Current | Suggestion |
|---------|------------|
| `border-radius: 0` | Use **`6px–10px`** on `.btn` for a modern but still professional look. |
| Flat colors | Add a **very subtle** `box-shadow` on primary/secondary; darken on `:hover` / `:active`. |
| Focus | Add **`:focus-visible`** outlines (`outline: 2px solid …; outline-offset: 2px`) so keyboard users match WCAG; avoid removing focus styles. |

Feature cards invert primary hover to `#0D0D0B` (lines ~121–122); keep that behavior but ensure the resting state still looks like one system with the rest of the buttons.

---

## 4. Main nav (`#navMain`, `#navbarMain`, `#navMainAppt`)

| Current | Suggestion |
|---------|------------|
| Heavy shadow `0 0 25px rgba(0,0,0,0.2)` | Softer: **`0 4px 24px rgba(13,13,11,0.08)`** (tied to `--color-dark`). |
| Nav link hover: full gold block | Slightly more current: **underline or bottom border** + color change, or a **light gold background** (`rgba(191, 186, 61, 0.15)`) instead of solid `#BFBA3D` so it’s less loud. |
| `#navMainAppt` | Same radius as buttons; slightly **more vertical padding** for touch targets (min ~44px height on small screens when visible). |

`#navMainAppt` is `display: none` in base CSS—confirm `page-helper.js` or media queries show it where intended; polish the visible state when you enable it.

---

## 5. Hero (`.hero`, `.hero-short`, `#HmHero`, etc.)

| Current | Suggestion |
|---------|------------|
| Large top padding (`380px` desktop) | Works with fixed image height; optionally add **`linear-gradient`** overlay via `background-image` layering (multiple backgrounds: gradient + `url(...)`) so **white `h1` text** stays readable on busy photos. |
| `min-height: 600px` | Consider **`min-height: 56vh`** on large screens as an alternative so fold height adapts; test with each page hero (`#AbHero`, `#CtHero`, …). |

---

## 6. Home features (`#HmSecFeatures`, `.feature`)

| Current | Suggestion |
|---------|------------|
| Flat white cards on `#F0ECDF` | Light **border** `1px solid rgba(13,13,11,0.06)` or **soft shadow** on `.feature` so cards lift slightly. |
| `.feature-header` solid `#0D0D0B` | Optional **very subtle** inner shadow or border-radius on the **image container** only (top corners if you radius the card). |

---

## 7. Testimonials (`#HmSecTestimonials`, `blockquote`)

| Current | Suggestion |
|---------|------------|
| Huge `.quote-mark` | Slightly reduce **opacity** (e.g. `0.35`) or size so the quote text competes visually. |
| Layout | Ensure `.col-content-container` padding works with rounded images; optional **border-radius** on blockquote container for consistency with cards. |

---

## 8. Footer (`#Ft`, `.bg-dark`)

| Current | Suggestion |
|---------|------------|
| `#0D0D0B` | Slight **top border** or padding increase (`48px`–`56px`) to separate from content. |
| Link color `#89A5A5` | Slightly brighter hover (you already go to gold); add **`:focus-visible`** for keyboard users. |

---

## 9. Locations UI (`#accordionLocations`, `.location-marker`, `#MapContainer`)

| Current | Suggestion |
|---------|------------|
| Accordion: `border-radius: 0` everywhere | **Radius on `.card`** (e.g. `8px`) and **overflow: hidden** on the card so headers look like one surface. |
| `.card-header` flat | Subtle **border-bottom** only between items instead of heavy grid feel. |
| `.card-body` scrollbar | Keep; optional **thinner** scrollbar or `scrollbar-color` for Firefox to match teal palette. |
| `.location-marker` circle | Slight **shadow** or border so it pops on `#c3d1d1` backgrounds. |

---

## 10. Practice details & group coupons (`#DtPracticeOverview`, `#accExtras`, `.coupon`)

| Current | Suggestion |
|---------|------------|
| Many `border-radius: 0` | Align with the same **`--radius-md`** as accordions and buttons for one visual language. |
| `.coupon` | Slightly **larger padding**, rounded corners, optional **left border accent** in `--color-primary` for scanability. |

---

## 11. Global accessibility (quick wins)

- **`a:focus-visible`, `button:focus-visible`, `.nav-link:focus-visible`:** visible ring, don’t rely on hover alone.
- **Contrast:** Body `#606051` on white is usually OK; verify gold `#BFBA3D` on **cream** `#F0ECDF` for small text (headlines only is safer).
- **`prefers-reduced-motion`:** optional `@media (prefers-reduced-motion: reduce)` to tone down hover transitions if you add `transition` on links/buttons.

---

## 12. Implementation order (low risk → higher touch)

1. **`:root` variables** + replace hex in **body, links, `.btn-primary`, `.bg-dark`, `.bg-light`** only.  
2. **Button radius + focus-visible** globally.  
3. **Nav shadow + softer link hover.**  
4. **Hero text overlay** (gradient) on one page, then replicate IDs.  
5. **Feature cards + accordion** radius and borders.  
6. **Footer + testimonial** tweaks.

---

## 13. What to avoid in a “quick” pass

- Rewriting every Bootstrap override (high regression risk).  
- Changing HTML structure or class names until you’re happy with CSS-only wins.  
- Loading many new font families (hurts performance); prefer **weights** first.

---

## 14. After you’re happy with CSS

- Update **`SITE_RECOVERY.md`** or README with a one-line note that `main.css` was modernized locally (optional).  
- Re-run **Lighthouse** (Accessibility + Performance) on home, locations, and contact.

---

*Document version: 1.1 — styles applied in repository; adjust tokens in `:root` as needed.*
