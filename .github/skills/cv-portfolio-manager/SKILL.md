---
name: cv-portfolio-manager
description: "CV, resume, and portfolio website management skill. Use when: creating new CV, updating existing CV, tailoring CV for job application, ATS optimization, LaTeX CV editing, portfolio website update, GitHub Pages deployment, adding projects to portfolio, web portfolio maintenance, HTML CSS JavaScript portfolio, resume formatting, cover letter, application materials, job-specific CV variant."
argument-hint: "What to do, e.g. 'create logistics CV for Harita Mineral', 'add new project to portfolio site'"
---

# CV & Portfolio Manager

Manage Reyza's CV collection (LaTeX) and live portfolio website. Create tailored variants, optimize for ATS, and maintain the GitHub Pages portfolio.

## When to Use
- Creating a new CV variant for a specific job application
- Updating existing CVs with new experience or achievements
- Tailoring CV keywords for ATS optimization
- Adding projects or skills to the portfolio website
- Deploying portfolio updates to GitHub Pages
- Formatting and styling improvements

## Workspace Structure
```
nicetomeetyou/
├── cv_qc_specialist.tex          # QC Digitalization Specialist CV (LaTeX)
├── cv_logistics_specialist.tex   # Logistics Specialist CV (LaTeX)
├── index.html                    # Main portfolio page
├── qc.html                       # QC-focused portfolio page
├── styles.css                    # Main stylesheet
├── SKILLS_PORTFOLIO_CSS.css      # Skills section styles
├── script.js                     # Portfolio JavaScript
├── email_harita_logistics.txt    # Application email for Harita
├── email_nsk_qc_digitalization.txt # Application email for NSK
├── images/                       # Image assets
│   ├── projects/                 # Project screenshots
│   └── tools/                    # Tool/tech logos
└── .github/skills/career-research/references/profile.md  # Master profile
```

## Procedure: Create New CV Variant

1. **Read the target job description** — extract required skills, keywords, qualifications
2. **Read master profile** at `.github/skills/career-research/references/profile.md`
3. **Choose base template** — use closest existing CV as starting point:
   - `cv_qc_specialist.tex` for quality/digitalization/developer roles
   - `cv_logistics_specialist.tex` for logistics/supply chain roles
4. **Tailor content**:
   - Reorder experience sections by relevance to target role
   - Adjust Professional Summary to match job language
   - Highlight achievements most relevant to the role
   - Add/emphasize skills matching job requirements
5. **ATS optimization**:
   - Mirror exact keywords from job posting
   - Include industry-standard terminology
   - Maintain clean LaTeX structure (no tables in skills section for ATS)
   - Update the white-text ATS keyword block at the bottom
6. **Save as new file**: `cv_[role_keyword].tex`

## Procedure: Update Existing CV

1. **Read the CV file** to understand current content
2. **Read profile.md** for latest career data
3. **Apply updates**:
   - Add new experience entries
   - Update date ranges
   - Add new skills or certifications
   - Refresh achievement numbers if updated
4. **Verify LaTeX compiles** — check for syntax errors
5. **Confirm changes with user** before saving

## Procedure: Portfolio Website Update

### Adding a New Project
1. Read `index.html` and/or `qc.html` to understand current structure
2. Read `SKILLS_PORTFOLIO_DATA_TEMPLATE.md` for data format
3. Add project card with:
   - Project title and description
   - Technologies used (with tool logos from `images/tools/`)
   - Key metrics/achievements
   - Screenshots (if available in `images/projects/`)
4. Update corresponding CSS if needed
5. Test responsiveness

### Updating Skills Section
1. Read `NEW_SKILLS_PORTFOLIO_SECTION.html` for current skills layout
2. Read `SKILLS_PORTFOLIO_CSS.css` for styling
3. Add/update skill entries maintaining existing design patterns
4. Ensure tool logos exist in `images/tools/` or note missing ones

### GitHub Pages Deployment
1. Verify all files are saved and consistent
2. Stage changes: `git add .`
3. Commit with descriptive message: `git commit -m "Update: [what changed]"`
4. Push to main branch: `git push origin main`
5. Verify deployment at the GitHub Pages URL

## LaTeX CV Structure (Template)
```latex
% Header: Name, title, contact info
% Professional Summary: 3-4 lines tailored to role
% Professional Experience: Reverse chronological, achievement-focused
% Technical Skills: Categorized by domain
% Education & Certification
% Key Achievements: Bullet highlights with numbers
% Relevant Project Examples: Brief project descriptions
% ATS Keywords: White-text block (invisible but parseable)
```

## ATS Optimization Checklist
- [ ] Job title in header matches or is close to posting title
- [ ] Summary uses key phrases from job description
- [ ] Skills section mirrors terminology from requirements
- [ ] Achievement bullets include quantified results
- [ ] Education and certifications are clearly listed
- [ ] White-text keyword block updated with role-specific terms
- [ ] File name includes role keyword for HR systems

## Constraints
- ALWAYS confirm CV changes with user before saving
- NEVER remove existing experience — only reorder or de-emphasize
- NEVER fabricate achievements or inflate numbers
- Maintain consistent LaTeX formatting across all CV variants
- Keep portfolio site responsive and accessible
- Test LaTeX compilation after edits when possible
