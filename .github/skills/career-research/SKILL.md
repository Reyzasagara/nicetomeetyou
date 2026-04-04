---
name: career-research
description: "Deep career research skill. Use when: researching a company before applying or interviewing, analyzing skill gaps for a target role, market intelligence gathering, industry trend analysis, competitor analysis, tech stack investigation, company culture research, Glassdoor reviews, LinkedIn insights, job market analysis Indonesia, global salary benchmarking, upskilling roadmap, learning path recommendation."
argument-hint: "Company name or role to research, e.g. 'PT Astra International - IT Manager'"
---

# Career Research

Deep research skill for career intelligence. Uses web browsing (Playwright) to gather real-time data about companies, roles, skill requirements, and market trends.

## When to Use
- Researching a company before applying or interviewing
- Analyzing skill gaps between current profile and target role
- Investigating industry trends and market opportunities
- Building an upskilling roadmap for a target career path
- Comparing job markets (Indonesia vs global)

## User Profile Reference
Always read [profile.md](./references/profile.md) first to ground research in Reyza's actual background.

## Procedure: Company Deep Dive

1. **Gather company basics** via web search:
   - Official website → mission, products, services, tech stack
   - LinkedIn company page → size, growth, recent hires, culture
   - Glassdoor → reviews, salary data, interview experiences
   - News articles → recent developments, funding, challenges

2. **Analyze the target role**:
   - Find the job posting (or similar postings at the company)
   - Extract required skills, qualifications, and responsibilities
   - Map against Reyza's profile → identify matches and gaps

3. **Compile intelligence report** with:
   - Company overview (industry, size, culture, tech stack)
   - Role analysis (requirements vs Reyza's profile match %)
   - Skill gaps with recommended upskilling resources
   - Interview insights from Glassdoor
   - Salary range estimates
   - Strategic talking points for application/interview

## Procedure: Skill Gap Analysis

1. **Define target role** — get the job description or role title
2. **Extract required skills** — categorize into: must-have, nice-to-have, bonus
3. **Map against profile** — read profile.md and workspace CVs
4. **Score match** — percentage match for each skill category
5. **Generate upskilling plan**:
   - Priority skills to learn (biggest gap + highest impact)
   - Recommended resources (courses, certifications, projects)
   - Estimated timeline for each skill
   - How to demonstrate the new skill (portfolio project, certification)

## Procedure: Market Intelligence

1. **Define scope** — industry, geography, role type
2. **Research salary ranges** — use Glassdoor, PayScale, LinkedIn Salary, local job boards
3. **Identify trending skills** — what employers are hiring for now
4. **Spot opportunities** — emerging roles, underserved niches, high-demand areas
5. **Compile report** with actionable recommendations

## Output Format

### Company Research Report
```
## [Company Name] – Research Report

### Company Overview
- Industry: ...
- Size: ... employees
- Location: ...
- Tech Stack: ...
- Culture: ...

### Role Analysis: [Target Role]
- Match Score: X%
- Strong Matches: [skills that align]
- Gaps: [skills to develop]

### Salary Intelligence
- Range: IDR X – Y / month (or USD)
- Source: [where data came from]

### Interview Insights
- Common questions reported
- Process description
- Tips from reviewers

### Strategic Recommendations
1. ...
2. ...
3. ...
```

## Web Research Guidelines
- Use Playwright MCP tools for browsing when available
- Always cite sources for salary data and company information
- Cross-reference multiple sources for accuracy
- Note when data is estimated vs reported
- Respect rate limits and robots.txt
