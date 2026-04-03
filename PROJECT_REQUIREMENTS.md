# Project Requirements: Pacific Dental Alliance Static Clone & GitHub Pages

## 1. Objective

Reproduce the public marketing site at [https://www.pacificdentalalliance.com/](https://www.pacificdentalalliance.com/) as a **static** website and **publish it on GitHub Pages** so it is reachable at a `*.github.io` URL (or a custom domain if configured later).

**Status:** A recovered static build lives in **`docs/`**. See **[SITE_RECOVERY.md](SITE_RECOVERY.md)** for ownership documentation, crawl procedure, and known limitations (contact `POST`, `photoviewer.ashx`, Maps API).

## 2. Source Reference

| Item | Detail |
|------|--------|
| Reference URL | https://www.pacificdentalalliance.com/ |
| Known primary sections (from live site) | Home hero, “Who We Are,” “Conveniently Located,” testimonial, “Find a Location” CTA, footer with navigation (Home, Our Story, Locations, Make an Appointment, Group Programs, Contact) |
| Top navigation | Our Story, Locations, Group Programs, Contact, Appointments |

The implementation should **match layout, typography hierarchy, colors, and copy** closely enough that a stakeholder would recognize it as the same brand experience. Exact pixel-perfect parity is desirable but not mandatory if minor differences are documented.

## 3. Scope

### 3.1 In scope

- **Pages or sections** implied by the reference site’s navigation and content blocks (at minimum: home; replicate linked destinations if they exist as separate URLs on the reference site).
- **Static assets**: images, icons, fonts (self-hosted or licensed web fonts), CSS, and any minimal client-side JS needed for menus or smooth behavior.
- **Responsive behavior**: usable on common mobile, tablet, and desktop widths.
- **Internal links** between sections/pages consistent with the reference site’s information architecture.
- **GitHub Pages–compatible output**: no server-side runtime (no PHP, Node server, or database at request time). Build tools (e.g. Vite, plain HTML) are allowed if the **deployed artifact** is static files only.
- **Repository**: code hosted on GitHub with Pages enabled (branch/folder per GitHub Pages settings: e.g. `main` + `/docs` or `gh-pages` or root on `main`).

### 3.2 Out of scope (unless explicitly added later)

- Backend forms that send email or store data (contact/appointment flows may be **static UI only** or link to external URLs as on the live site).
- CMS, authentication, or user accounts.
- SEO parity beyond reasonable defaults (title, meta description, semantic headings).
- Copying or mirroring **private** or **non-public** areas of any domain.

## 4. Technical Requirements

| Requirement | Description |
|-------------|-------------|
| Hosting | GitHub Pages |
| Delivery | HTTPS; no mixed-content warnings for assets |
| Performance | Reasonable load: optimized images (appropriate formats/sizes), avoid huge unoptimized assets |
| Accessibility | Semantic HTML where practical; visible focus for interactive elements; alt text on meaningful images |
| Browser support | Latest two major versions of Chrome, Firefox, Safari, and Edge (desktop and mobile where applicable) |
| Repository hygiene | README with local preview instructions, build steps (if any), and GitHub Pages deployment notes |

## 5. Legal & Content

- Confirm you have **permission** to reproduce branding, copy, and imagery, or use this project only for **private learning** with placeholder content. Unauthorized commercial reuse of another site’s assets may infringe copyright or trademark.
- If the reference site uses third-party fonts or stock images, retain or replace them according to license terms.

## 6. Acceptance Criteria

1. Visiting the GitHub Pages URL shows a home page that reflects the reference site’s main message (“A dental network to smile about,” value proposition, key sections, testimonial, and footer navigation).
2. All primary nav items resolve to the correct in-repo pages or in-page anchors, with no broken internal links.
3. Layout does not break at 320px, 768px, and 1280px widths (no horizontal scroll except where intentionally designed, e.g. wide tables if any).
4. Repository includes a clear **README**: how to run locally, how Pages is configured, and the live site URL.
5. Lighthouse (or manual check): no critical console errors on first load of the home page.

## 7. Deliverables

| Deliverable | Notes |
|-------------|--------|
| Source repository | HTML/CSS/JS (and optional build config) on GitHub |
| Published site | GitHub Pages URL documented in README |
| Optional | `LICENSE` file; `.gitignore` for OS/editor artifacts |

## 8. Suggested Implementation Order

1. Inventory reference pages and download or recreate assets (with rights cleared).
2. Implement global layout: header, footer, typography, color tokens.
3. Build home page section by section against the reference.
4. Add remaining pages from navigation.
5. Test responsiveness and internal links.
6. Configure GitHub Pages, push, verify production URL.

## 9. Open Questions (resolve before or during build)

- Which GitHub account/org will own the repo, and will the site use the default `username.github.io/repo` path or a custom domain?
- Should “Make an Appointment” / “Appointments” point to an external booking URL, a `mailto:` link, or a static placeholder?
- Are all subpages on the live site still reachable, and should each be cloned or consolidated?

---

**Document version:** 1.0  
**Reference site:** [Pacific Dental Alliance](https://www.pacificdentalalliance.com/)
