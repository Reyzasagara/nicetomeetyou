# Portfolio clarity update — 22 September 2026

Implemented from the supplied improvement specification, without changing official employment titles or adding achievements.

## Changes

- Business Analyst / Digital Transformation is the core positioning. The four other areas are supporting strengths; Business Analysis has the dominant capability card.
- Home order: hero, selected results, three flagship cases, capabilities, lab, career, about and contact. PowerSync comes first; Market Intelligence is the third case for the BA audience.
- Added bilingual `work.html` catalogs with the existing filters. Navigation, titles and accessible labels reflect capabilities instead of five job targets.
- Evidence registers use names from the actual evidence-directory index (not the illustrative code mappings in the specification), confidentiality status and interview availability. Removed standalone cryptic codes from illustration captions. Illustrations remain labeled summaries, not source screenshots.
- Replaced vendor-blaming copy and explicit security weaknesses with neutral assessment/rebuild wording. Removed the database-control weakness statement. No internal evidence files or operational screenshots were copied.
- Existing already-public metrics retained with their qualifiers. Added limits for the reviewed dataset and unknown legacy-import composition. Verification of source evidence does not establish employer permission to disclose it.
- CV experience bullets reduced from 17 to 12 (29%). Official titles and known dates retained. Engineering begins on page 2; cross-functional market work is identified as concurrent from 2024. EN and ID web CVs share the same content source; the downloadable PDF remains English and is labeled accordingly in ID.
- Contact links are clickable and larger. First-paint entrance/reveal animations removed for core content; reduced-motion support preserved.

## Files

Sources: `site-src/build.py`, `site-src/i18n_id.py`, `assets/presentation.css`.
Output: 30 EN/ID pages, including the two new work catalogs, and `assets/Reyza-Agung-Gunawan-CV.pdf`.
Tools: `site-src/validate.py`, `site-src/generate-pdf.cjs`, `.gitignore` (local previews and Python caches).

## Validation

- `python site-src/build.py`: 30 pages; all strings translated.
- `python site-src/validate.py`: local files and fragment links, unique heading IDs, homepage project count/order, email allowlist, internal-URL and disclosure regression checks pass.
- Browser QA in headless Edge: EN/ID at 1440 px and 390 px, no horizontal overflow; catalog filters, mobile menu and Escape behavior work. Keyboard focus reaches the skip link. No page JavaScript errors. Case heading visible with JavaScript disabled.
- PDF: two A4 pages, extractable/selectable text, contact hyperlinks, full engineering section starts on page 2. Both pages visually inspected.
- `git diff --check`: passes.
- Previews are local in `review-previews/`: EN/ID desktop/mobile, flagship case and both PDF pages. They are excluded from publication.
- External profile ownership, delivery of email and external sites' ongoing availability were not tested. Existing contact destinations are preserved.

## Factual review remaining

- Confirm the month of the 2026 official role transition; year-only dates remain.
- Confirm the review period of the 217 planned-versus-stamped pairs; no period invented.
- Confirm whether the 4,818 unit records include legacy imports and the breakdown; no new total inferred.
- Confirm employer approval for already-public operational counts, adoption/workload metrics and self-assessed security scores. This update retains these previously published figures, without claiming approval exists.

## Rebuild

Run `python site-src/build.py`, then `python site-src/validate.py`.
With Playwright available to Node and Microsoft Edge installed, run `node site-src/generate-pdf.cjs` from the repository root. Verify page count and preview both pages after CV changes.
