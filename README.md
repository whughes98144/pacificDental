# Pacific Dental Alliance — static site (GitHub Pages)

Recovered static copy of [pacificdentalalliance.com](https://www.pacificdentalalliance.com/) for deployment from the `docs/` folder.

## Design

- **[REDESIGN_V2.md](REDESIGN_V2.md)** — current visual direction (typography, palette, components). Styles live in `docs/_assets/css/main.css`.
- **[CSS_POLISH_SUGGESTIONS.md](CSS_POLISH_SUGGESTIONS.md)** — earlier incremental polish notes (mostly superseded by v2, still useful for token ideas).

## Documentation

- **[SITE_RECOVERY.md](SITE_RECOVERY.md)** — ownership note, what was recovered, limitations (forms, maps, photoviewer), and how to re-run the crawler.
- **[SITE_RECOVERY_LOG.md](SITE_RECOVERY_LOG.md)** — URL fetch log from the last `recover_site.py` run.
- **[PROJECT_REQUIREMENTS.md](PROJECT_REQUIREMENTS.md)** — original project requirements.

## Local preview

```bash
cd docs && python3 -m http.server 8080
```

Open `http://localhost:8080/`.

## Deploy to GitHub Pages

Repository **Settings → Pages**: source **branch** `main`, folder **`/docs`**.

## Regenerate from the live site

```bash
python3 scripts/recover_site.py
```

See [SITE_RECOVERY.md](SITE_RECOVERY.md) for details.
