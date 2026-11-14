---
name: source-research
description: Use when a fact must be established from sources (docs, papers, releases, data, news). Produces numbered, cited findings with confidence. Don't use for opinions, calculations or monitoring over time.
---

# Source research

## Procedure
1. **Frame:** write the exact question and what would count as an answer.
2. **Plan queries:** 3–6 varied search queries, including official names, version numbers and the current year.
3. **Source ranking:** primary (official docs, specs, papers, release notes, datasets, filings) > reputable secondary (major outlets, well-known experts) > everything else.
4. **Read, don't skim snippets.** Open each source you plan to cite.
5. **Extract:** for each claim, record the exact supporting sentence, the URL, the publication or retrieval date, and the source tier.
6. **Classify:** fact (directly stated) / inference (you derived it) / speculation.
7. **Triangulate:** important claims need two or more independent sources, or are marked single-source.
8. **Resolve conflicts:** prefer newer and more primary sources, and say why.
9. Run `citation-verification` on your own output.

## Output format
```
## Question
## Findings
1. <claim> — "<quote>" — <URL> (<date>) — [fact|inference|speculation] — [primary|secondary]
## Confidence   # per finding + why
## Gaps
## Verdict
```

## Checklist
- [ ] Every finding has a quote + URL
- [ ] Dates recorded
- [ ] Key claims triangulated or flagged single-source
- [ ] Gaps listed
