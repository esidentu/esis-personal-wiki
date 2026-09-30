# Search Mode Check

**Command:** `python wiki.py search "pricing"`

**Date:** 2026-09-29

## Result

Found 5 passages. No generated answer — search mode returns raw passages only.

### Passages Returned

1. **FTMBA 201A Economic Analysis Syllabus.txt** | Section: III Class Schedule | Relevance: highest
   - Contains lecture schedule including pricing topics, readings from Samuelson & Marks

2. **FTMBA 201A Economic Analysis Syllabus.txt** | Section: Course description | Relevance: high
   - Mentions "decision-making under uncertainty, economic costs, pricing, and the basics of strategic interactions between competitors"

3. **Data and Decisions Syllabus.txt** | Section: AI Policy | Relevance: 36%
   - Lower relevance match

4. **CLAUDIA ESI DENTU RESUME.txt** | Section: Telecel/Vodafone experience | Relevance: moderate
   - Contains product strategy and fintech marketplace context

5. **FTMBA 201A Economic Analysis Syllabus.txt** | Section: Main | Relevance: 28%
   - Course title and metadata

## Assessment

- **Correct behavior:** Search returns raw passages with source paths and relevance scores
- **No LLM generation:** Confirmed — no generated answer, only retrieved passages
- **Source accuracy:** Top results correctly come from the Economic Analysis syllabus where pricing is a core topic
